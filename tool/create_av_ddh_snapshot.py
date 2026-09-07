#!/usr/bin/env python3
"""Create a compact snapshot of the included AV-DDH source files."""

from collections import Counter
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as mpimg

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "av_ddh_xray"
RAW_ROOT = DATA_ROOT / "raw"
OUTPUT = REPO_ROOT / "docs" / "av_ddh_snapshot.png"
SAMPLE_ID = "1080704"
XLSX_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def read_workbook(path):
    namespace = {"m": XLSX_NS}
    with ZipFile(path) as archive:
        shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        shared = [
            "".join(text.text or "" for text in item.iter(f"{{{XLSX_NS}}}t"))
            for item in shared_root.findall("m:si", namespace)
        ]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))

    rows = []
    for row in sheet.findall(".//m:sheetData/m:row", namespace):
        values = {}
        for cell in row.findall("m:c", namespace):
            value = cell.find("m:v", namespace)
            if value is None:
                continue
            text = value.text or ""
            if cell.attrib.get("t") == "s":
                text = shared[int(text)]
            values[cell.attrib["r"].rstrip("0123456789")] = text
        rows.append(values)

    header = rows[0]
    return [
        {header[column]: value for column, value in row.items() if column in header}
        for row in rows[1:]
    ]


def as_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalise_id(value):
    text = str(value).strip()
    return text[:-2] if text.endswith(".0") else text


def plot_snapshot(rows, image_paths):
    right_ai = [
        value for row in rows
        if (value := as_float(row.get("Rt Acetabular Index in Degrees"))) is not None
    ]
    left_ai = [
        value for row in rows
        if (value := as_float(row.get("Lt Acetabular Index in Degrees"))) is not None
    ]
    by_id = {normalise_id(row.get("File Number", "")): row for row in rows}
    sample = by_id.get(SAMPLE_ID, rows[0])

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("AV-DDH External Dataset Snapshot", fontsize=20, fontweight="bold")

    sample_path = next(
        (path for path in image_paths if path.stem == str(sample["File Number"])),
        None,
    )
    if sample_path:
        axes[0, 0].imshow(mpimg.imread(sample_path))
    axes[0, 0].set_title(f"Sample raw image: {sample['File Number']}", fontweight="bold")
    axes[0, 0].axis("off")

    bins = np.arange(0.5, 48.5, 1)
    axes[0, 1].hist(right_ai, bins=bins, alpha=0.65, label="Right hip", color="royalblue")
    axes[0, 1].hist(left_ai, bins=bins, alpha=0.65, label="Left hip", color="crimson")
    axes[0, 1].set(title="Manual Acetabular Index", xlabel="Acetabular Index (degrees)", ylabel="Count")
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.25)

    ddh_order = ("no ddh", "right ddh", "left ddh", "bilateral ddh")
    ddh_counts = Counter(str(row.get("DDH", "")).strip().lower() for row in rows)
    ddh_values = [ddh_counts[label] for label in ddh_order]
    bars = axes[1, 0].bar(ddh_order, ddh_values, color="mediumpurple", edgecolor="black")
    axes[1, 0].bar_label(bars, padding=3)
    axes[1, 0].set(title="DDH Reference Labels", ylabel="Images")
    axes[1, 0].tick_params(axis="x", rotation=30)
    axes[1, 0].grid(axis="y", alpha=0.25)

    completeness = [
        sum(as_float(row.get(column)) is not None for row in rows)
        for column in (
            "Rt Acetabular Index in Degrees",
            "Lt Acetabular Index in Degrees",
        )
    ]
    axes[1, 1].axis("off")
    axes[1, 1].text(
        0.05,
        0.95,
        "Dataset Summary:\n\n"
        f"Raw images: {len(image_paths):,}\n"
        f"Spreadsheet rows: {len(rows):,}\n"
        f"JPG images: {sum(path.suffix.lower() == '.jpg' for path in image_paths):,}\n"
        f"PNG images: {sum(path.suffix.lower() == '.png' for path in image_paths):,}\n\n"
        f"Right AI mean: {np.mean(right_ai):.1f}°\n"
        f"Left AI mean: {np.mean(left_ai):.1f}°\n"
        f"Right AI missing: {len(rows) - completeness[0]}\n"
        f"Left AI missing: {len(rows) - completeness[1]}",
        transform=axes[1, 1].transAxes,
        va="top",
        fontsize=13,
        family="monospace",
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "whitesmoke", "edgecolor": "gray"},
    )

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=250, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    if not RAW_ROOT.is_dir() or not (DATA_ROOT / "data.xlsx").is_file():
        raise SystemExit(f"Expected AV-DDH files under {DATA_ROOT}")
    image_paths = sorted(
        path for path in RAW_ROOT.iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
    rows = read_workbook(DATA_ROOT / "data.xlsx")
    image_ids = {path.stem for path in image_paths}
    row_ids = {normalise_id(row.get("File Number", "")) for row in rows}
    if image_ids != row_ids:
        raise SystemExit("Image/metadata IDs do not match")
    plot_snapshot(rows, image_paths)
    print(f"Snapshot saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
