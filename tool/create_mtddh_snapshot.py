#!/usr/bin/env python3
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# --------------------------------------------
# CONSTANTS
# --------------------------------------------
ROOT_DIR = Path(
    "/home/adam/protected-experiments/xray-experiments/retuve-data/testing-manual/"
)
OUTDIR = Path("docs")
YOLO_IMAGE_PATH = Path("./mtddh_xray_2d/data/dataset1_train_h69.jpg")
YOLO_LABEL_PATH = YOLO_IMAGE_PATH.with_suffix(".txt")


# --------------------------------------------
# DATA LOADING UTILITIES
# --------------------------------------------
def find_metrics_files(root: Path) -> Dict[str, Path]:
    """Return mapping of relative paths to metrics.json paths under root."""
    files: Dict[str, Path] = {}
    for dirpath, _, filenames in os.walk(root):
        if "metrics.json" in filenames:
            fullpath = Path(dirpath) / "metrics.json"
            rel = os.path.relpath(fullpath, root)
            files[rel] = fullpath
    return files


def load_metrics_file(path: Path) -> Dict[str, float]:
    """Load metrics.json, returns a flat dict: {metric_name: value}."""
    with open(path, "r") as f:
        data = json.load(f)
    metrics: Dict[str, float] = {}
    for item in data.get("metrics", []):
        if isinstance(item, dict) and len(item) == 1:
            key, value = next(iter(item.items()))
            metrics[key] = value
    return metrics


def split_side_key(key: str) -> Tuple[str, Optional[str]]:
    """Split keys like 'ace_index_left' -> ('ace_index', 'left')."""
    for side in ("left", "right"):
        suffix = f"_{side}"
        if key.endswith(suffix):
            return key[: -len(suffix)], side
    return key, None


def build_case_side_rows(
    rel_path: str, metrics: Dict[str, float]
) -> List[Dict[str, object]]:
    """Build one or two rows (left/right) for this case."""
    sides_present = {
        split_side_key(k)[1] for k in metrics if split_side_key(k)[1]
    }
    sides_list = sorted(sides_present) if sides_present else [None]

    rows: List[Dict[str, object]] = []
    folder = os.path.basename(os.path.dirname(rel_path))
    for side in sides_list:
        row: Dict[str, object] = {
            "case_rel": rel_path,
            "folder": folder,
            "side": side if side is not None else "both",
        }
        for k, v in metrics.items():
            base_key, key_side = split_side_key(k)
            if key_side is None or key_side == side:
                row[base_key] = v
        rows.append(row)
    return rows


def build_dataframe(root: Path) -> pd.DataFrame:
    files = find_metrics_files(root)
    all_rows: List[Dict[str, object]] = []
    for rel, path in files.items():
        try:
            m = load_metrics_file(path)
            rows = build_case_side_rows(rel, m)
            all_rows.extend(rows)
        except Exception as e:
            print(f"Warning: failed to load {path}: {e}")

    df = pd.DataFrame(all_rows)
    for col in ["ace_index", "wiberg_index", "ihdi_grade", "tonnis_grade"]:
        if col not in df.columns:
            df[col] = np.nan
    return df


# --------------------------------------------
# YOLO VISUALIZATION UTILITIES
# --------------------------------------------
def load_yolo_pose_label(label_path: Path):
    poses = []
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            cls, xc, yc, w, h = int(parts[0]), *map(float, parts[1:5])
            keypoints = []
            for i in range(5, len(parts), 3):
                try:
                    keypoints.append(
                        (
                            float(parts[i]),
                            float(parts[i + 1]),
                            int(float(parts[i + 2])),
                        )
                    )
                except IndexError:
                    break
            poses.append((cls, xc, yc, w, h, keypoints))
    return poses


def draw_yolo_pose_on_ax(ax, image_path: Path, label_path: Path):
    """Draws a YOLO pose visualization directly onto a Matplotlib axis."""
    image = cv2.imread(str(image_path))
    if image is None:
        ax.text(0.5, 0.5, "Image not found", ha="center", va="center")
        ax.axis("off")
        return

    h, w = image.shape[:2]
    poses = load_yolo_pose_label(label_path)

    for cls, xc, yc, bw, bh, keypoints in poses:
        x1, y1 = int((xc - bw / 2) * w), int((yc - bh / 2) * h)
        x2, y2 = int((xc + bw / 2) * w), int((yc + bh / 2) * h)
        color = (0, 255, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            image,
            f"class {cls}",
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1,
        )

        for idx, (xk, yk, vk) in enumerate(keypoints):
            if vk == 0:
                continue
            px, py = int(xk * w), int(yk * h)
            color = (0, 0, 255) if vk == 1 else (255, 0, 0)
            cv2.circle(image, (px, py), 3, color, -1)
            cv2.putText(
                image,
                str(idx),
                (px + 5, py - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                1,
            )

    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax.axis("off")


# --------------------------------------------
# SNAPSHOT PLOTTING
# --------------------------------------------
def ensure_outdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def plot_snapshot(df: pd.DataFrame, outdir: Path):
    ensure_outdir(outdir)

    # Feature engineering for plots
    tokens = df["folder"].astype(str).str.split("_", expand=True)
    df["folder_group_letter"] = (
        tokens[tokens.columns[-1]]
        .astype(str)
        .str.extract(r"([A-Za-z])", expand=False)
        .str.lower()
    )
    df_plot = df[~df["folder_group_letter"].isin(["i", "z"])]

    # Identify and print files with ace_index over 80
    high_ace_indices = df_plot[df_plot["ace_index"] > 80]
    if not high_ace_indices.empty:
        print("Files with ace_index > 80 (removed from plot):")
        for _, row in high_ace_indices.iterrows():
            print(
                f"- {row['case_rel']} (side: {row['side']}, ACE: {row['ace_index']})"
            )
    df_plot = df_plot[df_plot["ace_index"] <= 80]

    # Main plot generation
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("MTDDH Dataset Snapshot", fontsize=16)

    # A: Distributions
    ax = axs[0]
    for col in ["ace_index", "wiberg_index"]:
        if col in df_plot.columns:
            data = df_plot[col].dropna()
            mean_val = data.mean()
            std_val = data.std()
            label = f"{col} (μ={mean_val:.1f}, σ={std_val:.1f})"
            sns.kdeplot(data, ax=ax, fill=True, alpha=0.3, label=label)
    ax.set_title("Distributions")
    ax.legend()

    # B: Scatter ACE vs Wiberg
    ax = axs[1]
    if {"ace_index", "wiberg_index"}.issubset(df_plot.columns):
        sns.scatterplot(
            data=df_plot,
            x="ace_index",
            y="wiberg_index",
            hue="ihdi_grade",
            ax=ax,
            s=30,
        )
        ax.set_title("ACE vs Wiberg Index")

    # C: Grade Counts
    ax = axs[2]
    grades_df = df_plot[["ihdi_grade", "tonnis_grade"]].melt(
        var_name="Grade Type", value_name="Grade"
    )
    sns.countplot(data=grades_df, x="Grade", hue="Grade Type", ax=ax)
    ax.set_title("Grade Counts")

    # Add exact count numbers for grades 2, 3, and 4
    # Get the patches from the plot
    patches = ax.patches
    grade_types = grades_df["Grade Type"].unique()
    grades = sorted(grades_df["Grade"].unique())

    # Calculate the width of each bar
    bar_width = patches[0].get_width()

    # Add text annotations for grades 2, 3, and 4
    for i, grade_type in enumerate(grade_types):
        for grade in [2, 3, 4]:
            count = df_plot[df_plot[grade_type] == grade].shape[0]
            if count > 0:
                # Find the position for this grade and type
                grade_idx = grades.index(grade)
                x_pos = (
                    grade_idx
                    - (len(grade_types) - 1) * bar_width / 2
                    + i * bar_width
                )

                ax.text(
                    x_pos,
                    count + 0.5,
                    str(count),
                    ha="center",
                    va="bottom",
                    color="black",
                )

    plt.tight_layout(rect=[0, 0, 0.95, 0.95])
    plt.savefig(outdir / "mtddh_snapshot_new.png", dpi=250)
    plt.close()


# --------------------------------------------
# MAIN EXECUTION
# --------------------------------------------
def main():
    if not ROOT_DIR.exists():
        raise SystemExit(f"Root directory not found: {ROOT_DIR}")

    print(f"Loading metrics from: {ROOT_DIR}")
    df = build_dataframe(ROOT_DIR)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")

    print("Creating snapshot plots...")
    plot_snapshot(df, OUTDIR)
    print(f"Snapshot saved under: {OUTDIR}")

    print("Done.")


if __name__ == "__main__":
    main()
