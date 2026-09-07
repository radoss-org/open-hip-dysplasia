#!/usr/bin/env python3
"""
Radiopedia Ultrasound Dataset Snapshot Generator

This script analyzes the Radiopedia ultrasound dataset and creates
a comprehensive visualization snapshot showing key dataset characteristics.
"""

import json
import os
import re
import warnings
from collections import Counter, defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image

warnings.filterwarnings("ignore")

# Set style for consistent plots
plt.style.use("default")
sns.set_palette("husl")


def parse_numeric_value(value):
    """Parse numeric values that might contain ranges or special characters"""
    if pd.isna(value) or value == "NaN" or value is None:
        return np.nan

    if isinstance(value, (int, float)):
        return float(value)

    value_str = str(value).strip()

    # Handle ranges like "0.30-0.40" or ">0.50"
    if "-" in value_str and not value_str.startswith("-"):
        parts = value_str.split("-")
        return (float(parts[0]) + float(parts[1])) / 2

    # Handle greater than symbols
    if value_str.startswith(">"):
        return float(value_str[1:])

    # Handle approximately symbols
    if value_str.startswith("~"):
        return float(value_str[1:])

    # Try to extract first number from the string
    numbers = re.findall(r"\d+\.?\d*", value_str)
    if numbers:
        return float(numbers[0])

    return np.nan


def parse_age_to_months(age_str):
    """Convert age string to months"""
    if pd.isna(age_str) or age_str == "NaN":
        return np.nan

    age_str = str(age_str).lower()

    if "day" in age_str:
        days = int(re.findall(r"\d+", age_str)[0])
        return days / 30.44  # Average days per month
    elif "week" in age_str:
        weeks = int(re.findall(r"\d+", age_str)[0])
        return weeks / 4.345  # Average weeks per month
    elif "month" in age_str:
        months = int(re.findall(r"\d+", age_str)[0])
        return months
    elif "year" in age_str:
        years = int(re.findall(r"\d+", age_str)[0])
        return years * 12

    return np.nan


def load_dataset_info():
    """Load and parse all JSON files from the dataset"""
    data_dir = "./radiopedia_ultrasound_2d/data"
    json_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]

    dataset = []
    for json_file in json_files:
        with open(os.path.join(data_dir, json_file), "r") as f:
            data = json.load(f)
            dataset.append(data)

    return dataset


def plot_observed_counts(ax, series, title, xlabel, colors, log_y=False):
    counts = pd.concat(
        {label: values.value_counts() for label, values in series.items()}, axis=1
    ).fillna(0).sort_index()
    positions = np.arange(len(counts))
    width = 0.8 / len(series)

    for index, (label, color) in enumerate(colors.items()):
        offset = (index - (len(series) - 1) / 2) * width
        bars = ax.bar(
            positions + offset,
            counts[label],
            width=width,
            label=label if len(series) > 1 else None,
            color=color,
            alpha=0.7,
            edgecolor="black",
        )
        ax.bar_label(
            bars,
            labels=[str(int(value)) if value else "" for value in counts[label]],
            padding=3,
            fontsize=9,
        )

    ax.set_xticks(positions, [f"{value:g}" for value in counts.index])
    ax.set_title(title, fontweight="bold", fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Count")
    if log_y:
        ax.set_yscale("log")
        ax.set_ylim(bottom=0.8)
    if len(series) > 1:
        ax.legend()
    ax.grid(True, alpha=0.3)


def create_snapshot():
    """Create simplified dataset snapshot with specific requested elements"""
    # Load dataset
    dataset = load_dataset_info()

    # Convert to DataFrame for easier analysis
    rows = []
    for item in dataset:
        row_data = item["row_data"].copy()
        row_data["side"] = item["side"]
        row_data["filename"] = item["filename"]
        rows.append(row_data)

    df = pd.DataFrame(rows)

    # Clean up NaN strings in the dataframe
    df = df.replace("NaN", np.nan)

    # Parse numeric columns
    df["Alpha_Angle_R_num"] = df["R Alpha Angle"].apply(parse_numeric_value)
    df["Alpha_Angle_L_num"] = df["L Alpha Angle"].apply(parse_numeric_value)
    df["Beta_Angle_R_num"] = df["R Beta Angle"].apply(parse_numeric_value)
    df["Beta_Angle_L_num"] = df["L Beta Angle"].apply(parse_numeric_value)
    df["Coverage_R_num"] = df["R Coverage"].apply(parse_numeric_value)
    df["Coverage_L_num"] = df["L Coverage"].apply(parse_numeric_value)
    df["Age_months"] = df["Age"].apply(parse_age_to_months)

    # Create figure with specific layout
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle(
        "Radiopedia Ultrasound Dataset Snapshot",
        fontsize=20,
        fontweight="bold",
        y=0.95,
    )

    # 1. Display the specific image
    ax1 = plt.subplot(2, 3, 1)
    try:
        img_path = "./docs/172535_0_labels.jpg"
        img = Image.open(img_path)
        ax1.imshow(img)
        ax1.set_title("Sample Labeled Image", fontweight="bold", fontsize=14)
        ax1.axis("off")
    except Exception as e:
        ax1.text(
            0.5,
            0.5,
            f"Image not found:\n{img_path}",
            ha="center",
            va="center",
            transform=ax1.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"),
        )
        ax1.set_title("Sample Labeled Image", fontweight="bold", fontsize=14)
        ax1.axis("off")

    # 2. Age Distribution
    ax2 = plt.subplot(2, 3, 2)
    valid_ages = df["Age_months"].dropna()
    plot_observed_counts(
        ax2,
        {"Images": valid_ages.round(2)},
        "Age Distribution",
        "Age (months)",
        {"Images": "skyblue"},
    )

    # 3. Alpha Angle Distribution (Combined)
    ax3 = plt.subplot(2, 3, 3)
    alpha_r = df["Alpha_Angle_R_num"].dropna()
    alpha_l = df["Alpha_Angle_L_num"].dropna()
    plot_observed_counts(
        ax3,
        {"Right Hip": alpha_r, "Left Hip": alpha_l},
        "Alpha Angle Distribution",
        "Alpha Angle (degrees)",
        {"Right Hip": "blue", "Left Hip": "red"},
        log_y=True,
    )

    # 4. Graf Type Distribution (Correct Side Only)
    ax4 = plt.subplot(2, 3, 4)
    # Only use Graf type for the side that the image actually shows
    graf_correct_side = []
    for _, row in df.iterrows():
        if row["side"] == "right" and pd.notna(row["R Graf Type"]):
            graf_correct_side.append(row["R Graf Type"])
        elif row["side"] == "left" and pd.notna(row["L Graf Type"]):
            graf_correct_side.append(row["L Graf Type"])

    graf_counts = pd.Series(graf_correct_side).value_counts()
    ax4.bar(
        graf_counts.index,
        graf_counts.values,
        width=0.9,
        color="lightgreen",
        alpha=0.7,
        edgecolor="black",
    )
    ax4.set_title(
        "Graf Type Distribution (Correct Side)", fontweight="bold", fontsize=14
    )
    ax4.set_xlabel("Graf Type")
    ax4.set_ylabel("Count")
    ax4.set_xticks(range(len(graf_counts)), graf_counts.index, rotation=45)
    ax4.set_yscale("log")
    ax4.set_ylim(bottom=0.8)
    plt.grid(True, alpha=0.3)

    # 5. Beta Angle Distribution (Combined)
    ax5 = plt.subplot(2, 3, 5)
    beta_r = df["Beta_Angle_R_num"].dropna()
    beta_l = df["Beta_Angle_L_num"].dropna()
    plot_observed_counts(
        ax5,
        {"Right Hip": beta_r, "Left Hip": beta_l},
        "Beta Angle Distribution",
        "Beta Angle (degrees)",
        {"Right Hip": "green", "Left Hip": "orange"},
    )

    # 6. Dataset Summary
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis("off")

    # Calculate summary statistics
    total_images = len(df)
    unique_patients = len(df["RadID"].unique())
    age_range = f"{valid_ages.min():.1f} - {valid_ages.max():.1f} months"
    mean_age = f"{valid_ages.mean():.1f} months"

    # Calculate breech presentation percentage
    breech_counts = df["Breech?"].value_counts()
    total_breech_known = breech_counts.sum()
    breech_yes = breech_counts.get("Y", 0)
    breech_percentage = (
        (breech_yes / total_breech_known * 100)
        if total_breech_known > 0
        else 0
    )
    breech_completeness = total_breech_known / total_images * 100

    summary_text = f"""Dataset Summary:

Total Images: {total_images}
Unique Patients: {unique_patients}
Age Range: {age_range}
Mean Age: {mean_age}

Gender Distribution:
Male: {len(df[df['Gender'] == 'M'])} ({len(df[df['Gender'] == 'M'])/total_images*100:.1f}%)
Female: {len(df[df['Gender'] == 'F'])} ({len(df[df['Gender'] == 'F'])/total_images*100:.1f}%)

Breech Presentation: {breech_percentage:.1f}% (of known cases)
Breech Data Available: {breech_completeness:.1f}%

Data Completeness:
Alpha Angles: {((~df['Alpha_Angle_R_num'].isna()).sum() + (~df['Alpha_Angle_L_num'].isna()).sum())/(total_images*2)*100:.1f}%
Beta Angles: {((~df['Beta_Angle_R_num'].isna()).sum() + (~df['Beta_Angle_L_num'].isna()).sum())/(total_images*2)*100:.1f}%
Coverage: {((~df['Coverage_R_num'].isna()).sum() + (~df['Coverage_L_num'].isna()).sum())/(total_images*2)*100:.1f}%
Breech: {(~df['Breech?'].isna()).sum()/total_images*100:.1f}%
"""

    plt.text(
        0.05,
        0.95,
        summary_text,
        transform=ax6.transAxes,
        fontsize=11,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8),
    )

    plt.tight_layout(pad=0.5)
    plt.subplots_adjust(top=0.90, hspace=0.15, wspace=0.18)

    # Save the plot
    output_path = "./docs/radiopedia_snapshot.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Simplified snapshot saved to: {output_path}")

    # Display key statistics
    print("\n" + "=" * 60)
    print("RADIOPEDIA ULTRASOUND DATASET SUMMARY")
    print("=" * 60)
    print(f"Total Images: {total_images}")
    print(f"Unique Patients: {unique_patients}")
    print(f"Age Range: {age_range}")
    print(f"Mean Age: {mean_age}")
    print(f"Breech Presentation: {breech_percentage:.1f}% (of known cases)")
    print(f"Breech Data Available: {breech_completeness:.1f}%")
    print(
        f"Most Common Graf Type: {graf_counts.index[0]} ({graf_counts.iloc[0]} cases)"
    )
    print(
        f"Alpha Angle Range: {min(alpha_r.min(), alpha_l.min()):.1f} - {max(alpha_r.max(), alpha_l.max()):.1f} degrees"
    )
    print(
        f"Beta Angle Range: {min(beta_r.min(), beta_l.min()):.1f} - {max(beta_r.max(), beta_l.max()):.1f} degrees"
    )
    print("=" * 60)

    plt.show()

    return df


if __name__ == "__main__":
    # Create the snapshot
    df = create_snapshot()
