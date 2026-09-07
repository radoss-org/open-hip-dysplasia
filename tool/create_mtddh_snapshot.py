#!/usr/bin/env python3
"""Create a compact snapshot of the MTDDH working-set metrics."""

import json
import os
import re
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import image as mpimg
import numpy as np
import pandas as pd
import seaborn as sns

METRIC_COLUMNS = ("ace_index", "wiberg_index", "ihdi_grade", "tonnis_grade")
METRIC_LABELS = {
    "ace_index": "Acetabular Index",
    "wiberg_index": "Wiberg Index",
    "ihdi_grade": "International Hip Dysplasia Institute Grade",
    "tonnis_grade": "Tönnis Grade",
}
LANDMARK_LABELS = {
    "pel_l_o": "Image-left outer pelvic point",
    "pel_l_i": "Image-left inner pelvic point",
    "fem_l": "Image-left femur landmark",
    "h_point_l": "Image-left H-point",
    "pel_r_o": "Image-right outer pelvic point",
    "pel_r_i": "Image-right inner pelvic point",
    "fem_r": "Image-right femur landmark",
    "h_point_r": "Image-right H-point",
}
LETTER_GROUPS = {
    "a": "a",
    "b": "b/c/w/y",
    "c": "b/c/w/y",
    "w": "b/c/w/y",
    "y": "b/c/w/y",
    "e": "e/h",
    "h": "e/h",
    "d": "d/l/o",
    "l": "d/l/o",
    "o": "d/l/o",
}
METRICS_ROOT = Path(
    os.environ.get("MTDDH_METRICS_ROOT", "retuve-data/testing-manual")
)
REPO_ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = REPO_ROOT / "mtddh_xray_2d" / "data"
SAMPLE_CASE = "dataset1_validation_h99"
OUTDIR = REPO_ROOT / "docs"
OUTPUT_NAME = "mtddh_snapshot.png"


def load_case(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def flatten_metrics(data):
    return {
        key: value
        for item in data.get("metrics", [])
        if isinstance(item, dict) and len(item) == 1
        for key, value in item.items()
    }


def load_metrics(path):
    return flatten_metrics(load_case(path))


def split_side_key(key):
    for side in ("left", "right"):
        suffix = f"_{side}"
        if key.endswith(suffix):
            return key[: -len(suffix)], side
    return key, None


def case_side_rows(path, root, metrics):
    parsed_keys = {key: split_side_key(key) for key in metrics}
    sides = sorted({side for _, side in parsed_keys.values() if side}) or [None]
    rows = []

    for side in sides:
        row = {
            "case_rel": str(path.relative_to(root)),
            "folder": path.parent.name,
            "side": side or "both",
        }
        for key, value in metrics.items():
            base_key, key_side = parsed_keys[key]
            if key_side is None or key_side == side:
                row[base_key] = value
        rows.append(row)
    return rows


def build_dataframe(root):
    paths = sorted(root.rglob("metrics.json"))
    rows = []
    for path in paths:
        try:
            rows.extend(case_side_rows(path, root, load_metrics(path)))
        except Exception as error:
            print(f"Warning: failed to load {path}: {error}")

    df = pd.DataFrame(rows)
    for column in METRIC_COLUMNS:
        if column not in df:
            df[column] = np.nan
    return df, len(paths)


def load_sample(root):
    metrics_path = root / SAMPLE_CASE / "metrics.json"
    raw_path = IMAGE_ROOT / f"{SAMPLE_CASE}.jpg"
    output_path = root / SAMPLE_CASE / "img.jpg"
    if not metrics_path.exists():
        return None, None, None
    return (
        mpimg.imread(raw_path) if raw_path.exists() else None,
        mpimg.imread(output_path) if output_path.exists() else None,
        load_case(metrics_path),
    )


def plot_image(ax, image, title):
    if image is None:
        ax.text(0.5, 0.5, f"{SAMPLE_CASE} not available", ha="center", va="center")
        ax.axis("off")
        return

    ax.imshow(image, cmap="gray")
    ax.set_title(title)
    ax.axis("off")


def plot_landmarks(ax, image, landmarks):
    plot_image(ax, image, f"Retuve landmarks (image direction): {SAMPLE_CASE}")
    if image is None or not landmarks:
        return

    for side, x, ha in (("l", 0.02, "left"), ("r", 0.98, "right")):
        names = [
            name
            for name in LANDMARK_LABELS
            if f"_{side}_" in name or name.endswith(f"_{side}")
        ]
        for y_fraction, name in zip((0.16, 0.36, 0.56, 0.76), names):
            point = landmarks.get(name)
            if not point:
                continue
            point_x, point_y = point
            color = "#ff3b30" if side == "l" else "#1683ff"
            ax.scatter(
                point_x,
                point_y,
                s=28,
                c=color,
                edgecolors="white",
                linewidths=0.8,
                zorder=3,
            )
            ax.annotate(
                LANDMARK_LABELS[name],
                xy=(point_x, point_y),
                xycoords="data",
                xytext=(x, y_fraction),
                textcoords=ax.transAxes,
                ha=ha,
                va="center",
                color="white",
                fontsize=8,
                weight="bold",
                bbox={
                    "boxstyle": "round,pad=0.25",
                    "facecolor": "black",
                    "edgecolor": color,
                    "alpha": 0.82,
                },
                arrowprops={"arrowstyle": "-", "color": color, "lw": 1.0},
                annotation_clip=False,
                zorder=4,
            )


def plot_letter_confusion(ax, df):
    cases = df[df["folder"].str.startswith("dataset1_")].groupby("folder")[
        "ihdi_grade"
    ].max().reset_index()
    cases["letter"] = (
        cases["folder"].str.rsplit("_", n=1).str[-1]
        .str.extract(r"([A-Za-z])\d*$", expand=False)
        .str.lower()
    )
    cases = cases.dropna(subset=["letter"])
    cases["letter_group"] = cases["letter"].map(LETTER_GROUPS)
    matrix = pd.crosstab(cases["letter_group"], cases["ihdi_grade"])
    matrix = matrix.reindex(
        index=list(dict.fromkeys(LETTER_GROUPS.values())), fill_value=0
    )
    matrix = matrix.reindex(columns=[1, 2, 3, 4], fill_value=0).astype(int)
    sns.heatmap(
        matrix,
        annot=True,
        annot_kws={"fontsize": 14, "fontweight": "bold"},
        fmt="d",
        cmap="Blues",
        cbar=False,
        ax=ax,
    )
    ax.set_title("Dataset 1 Letter Groups vs IHDI Grade")
    ax.set_xlabel("International Hip Dysplasia Institute Grade (max hip grade)")
    ax.set_ylabel("Dataset 1 letter group")


def plot_snapshot(df, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    all_df = df.copy()

    high_ace = df[df["ace_index"] > 80]
    if not high_ace.empty:
        print("Files with ace_index > 80 (removed from plots):")
        for _, row in high_ace.iterrows():
            print(f"- {row['case_rel']} (side: {row['side']}, ACE: {row['ace_index']})")

    df = df[df["ace_index"] <= 80].copy()
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle("MTDDH Dataset Snapshot", fontsize=16)
    axes[0, 0].set_title("Distributions")

    for column, limit in (("ace_index", 60), ("wiberg_index", 60)):
        data = df[column].dropna()
        if limit is not None:
            filtered = data[data <= limit]
            if len(filtered) != len(data):
                print(
                    f"Removed {len(data) - len(filtered)} "
                    f"{column} values > {limit} from distribution plot"
                )
            data = filtered
        sns.kdeplot(
            data,
            ax=axes[0, 0],
            fill=True,
            alpha=0.3,
            label=f"{METRIC_LABELS[column]} (μ={data.mean():.1f}, σ={data.std():.1f})",
        )
    axes[0, 0].set_xlabel("Metric value")
    axes[0, 0].set_xlim(right=60)
    axes[0, 0].legend(loc="upper right")

    scatter_limit = 100
    scatter_df = df[df["wiberg_index"] <= scatter_limit]
    if len(scatter_df) != len(df):
        print(
            f"Removed {len(df) - len(scatter_df)} rows with "
            f"{METRIC_LABELS['wiberg_index']} > {scatter_limit} "
            "from scatter plot"
        )
    sns.scatterplot(
        data=scatter_df,
        x="ace_index",
        y="wiberg_index",
        hue="ihdi_grade",
        ax=axes[0, 1],
        s=30,
    )
    axes[0, 1].set_title("Acetabular Index vs Wiberg Index")
    axes[0, 1].set_xlabel(METRIC_LABELS["ace_index"])
    axes[0, 1].set_ylabel(METRIC_LABELS["wiberg_index"])
    axes[0, 1].set_ylim(0, scatter_limit)
    axes[0, 1].legend(loc="upper left", title="IHDI Grade")

    grades = df[["ihdi_grade", "tonnis_grade"]].melt(
        var_name="Grade Type", value_name="Grade"
    )
    grades["Grade Type"] = grades["Grade Type"].map(METRIC_LABELS)
    sns.countplot(data=grades, x="Grade", hue="Grade Type", ax=axes[0, 2])
    axes[0, 2].set_title("Hip Grade Counts")
    for container in axes[0, 2].containers:
        labels = [
            str(int(bar.get_height())) if bar.get_height() else ""
            for bar in container
        ]
        axes[0, 2].bar_label(
            container,
            labels=labels,
            padding=3,
            fontsize=14,
            fontweight="bold",
        )

    image, output_image, sample = load_sample(METRICS_ROOT)
    landmarks = sample.get("landmarks") if sample else None
    plot_landmarks(axes[1, 0], image, landmarks)
    plot_image(
        axes[1, 1],
        output_image,
        f"Example Retuve output (.jpg): {SAMPLE_CASE}",
    )
    plot_letter_confusion(axes[1, 2], all_df)

    fig.tight_layout(rect=[0, 0, 0.95, 0.95])
    fig.savefig(outdir / OUTPUT_NAME, dpi=250)
    plt.close(fig)


def main():
    if not METRICS_ROOT.is_dir():
        raise SystemExit(
            f"Metrics directory not found: {METRICS_ROOT}. "
            "Set MTDDH_METRICS_ROOT to the directory containing metrics.json files."
        )

    print(f"Loading metrics from: {METRICS_ROOT}")
    df, metrics_file_count = build_dataframe(METRICS_ROOT)
    print(f"Loaded {len(df)} hip rows and {len(df.columns)} columns.")
    print(f"Total metrics.json files found: {metrics_file_count}")
    plot_snapshot(df, OUTDIR)
    print(f"Snapshot saved to: {OUTDIR / OUTPUT_NAME}")


if __name__ == "__main__":
    main()
