import json
import os
import re
from collections import defaultdict

MTDDH_EXTRACTED_LOCATION = (
    "/home/adam/experiments/old/xray-experiments/raw/MTDDH/"
)


def list_files_with_paths(directory):
    """Return a dictionary mapping base names to full paths from a directory."""
    file_map = {}
    for f in os.listdir(directory):
        full_path = os.path.join(directory, f)
        if os.path.isfile(full_path):
            base_name = os.path.splitext(f)[0]
            # Only store if it's a JPEG or if we haven't stored this base name yet
            if (
                f.lower().endswith((".jpg", ".jpeg"))
                or base_name not in file_map
            ):
                file_map[base_name] = full_path
    return file_map


def list_dataset2_files(base_directory):
    """Return a dictionary mapping first-level folder names to img.png paths."""
    file_map = {}

    # Iterate through first-level subdirectories
    for first_level in os.listdir(base_directory):
        first_level_path = os.path.join(base_directory, first_level)
        if not os.path.isdir(first_level_path):
            continue

        # Walk through all subdirectories to find img.png
        for root, dirs, files in os.walk(first_level_path):
            if "img.png" in files:
                img_path = os.path.join(root, "img.png")
                file_map[first_level] = img_path
                break  # Found img.png for this first-level folder

    return file_map


def clean_dataset1_prefix(base_name):
    """Remove dataset1 prefixes (train, validation, test) from base name."""
    return re.sub(r"^dataset1_(train|validation|test)_", "", base_name)


def extract_dataset2_id(file_name):
    """Extract the ID from dataset2 file names like dataset2_8dd741ed_img.png."""
    match = re.match(r"dataset2_([^_]+)_img", file_name)
    return match.group(1) if match else None


def load_json_files(json_paths):
    """Load JSON files and return a set of base names from file_name fields."""
    base_names = set()

    for json_path in json_paths:
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)

            # Extract base names from file_name fields
            for image in data.get("images", []):
                file_name = image.get("file_name", "")
                if file_name:
                    base_name = os.path.splitext(file_name)[0]
                    base_names.add(base_name)
        else:
            print(f"Warning: JSON file not found: {json_path}")

    return base_names


def analyze_missing_files(missing_files, json_base_names):
    """Analyze missing files and categorize them by reason for exclusion.

    Returns a dictionary where keys are exclusion reasons and values are lists of file names.
    Files that don't match any specific reason are categorized as 'unexplained'.
    """
    exclusion_reasons = defaultdict(list)

    for file_name in missing_files:
        # Reason 1: File missing from JSON files
        if file_name not in json_base_names:
            exclusion_reasons["missing_from_json"].append(file_name)
        else:
            # Default case: file is missing for reasons we haven't identified
            exclusion_reasons["processing errors"].append(file_name)

    return exclusion_reasons


def analyze_missing_files_simple(missing_files):
    """Categorize all missing files as unexplained."""
    exclusion_reasons = defaultdict(list)
    exclusion_reasons["processing errors"] = list(missing_files)
    return exclusion_reasons


def process_dataset(
    dataset_name, all_files_map, data_dir, json_base_names=None
):
    """Process a single dataset and print results."""
    # Get files from data_dir for this dataset
    data_files = set()

    for f in os.listdir(data_dir):
        full_path = os.path.join(data_dir, f)
        if not os.path.isfile(full_path):
            continue

        base_name = os.path.splitext(f)[0]

        if dataset_name == "dataset1":
            # Skip dataset2 images
            if "dataset2_" in base_name.lower():
                continue
            # Clean dataset1 prefixes
            base_name = clean_dataset1_prefix(base_name)
        else:  # dataset2
            # Only process dataset2 images
            if "dataset2_" not in base_name.lower():
                continue
            # Extract the ID
            extracted_id = extract_dataset2_id(base_name)
            if extracted_id:
                base_name = extracted_id

        data_files.add(base_name)

    # Compare sets in both directions
    missing_in_data_dir = sorted(set(all_files_map.keys()) - data_files)
    missing_in_all_files = sorted(data_files - set(all_files_map.keys()))
    matched_base_names = sorted(set(all_files_map.keys()) & data_files)

    # Analyze reasons for missing files
    if json_base_names is not None:
        exclusion_reasons = analyze_missing_files(
            missing_in_data_dir, json_base_names
        )
    else:
        exclusion_reasons = analyze_missing_files_simple(missing_in_data_dir)

    # Stats
    total_dataset_files = len(all_files_map)
    total_data_dir_files = len(data_files)
    total_matches = len(matched_base_names)
    total_missing_in_data_dir = len(missing_in_data_dir)
    total_missing_in_all_files = len(missing_in_all_files)
    total_json_files = len(json_base_names) if json_base_names else 0

    # Print summary stats
    print("\n==== FILE STATS ====")
    print(f"Total {dataset_name} files: {total_dataset_files}")
    print(
        f"Total data_dir ({dataset_name} only) files: {total_data_dir_files}"
    )
    print(f"Matched files: {total_matches}")
    print(f"Missing in data_dir: {total_missing_in_data_dir}")
    print(f"Missing in {dataset_name} mapping: {total_missing_in_all_files}")
    if json_base_names:
        print(f"Total files in JSONs: {total_json_files}")
    print("\nMissing files breakdown:")
    for reason, count in {
        reason: len(files) for reason, files in exclusion_reasons.items()
    }.items():
        print(f"  - {reason}: {count} files")
    print("====================")


def main():
    data_dir = "mtddh_xray_2d/data"

    # test_key = list_files_with_paths(
    #     f"{MTDDH_EXTRACTED_LOCATION}/Dataset1/Keypoints/Test"
    # )
    train_key = list_files_with_paths(
        f"{MTDDH_EXTRACTED_LOCATION}/Dataset1/Keypoints/Train"
    )
    val_key = list_files_with_paths(
        f"{MTDDH_EXTRACTED_LOCATION}/Dataset1/Keypoints/Validation"
    )

    # test_reg = list_files_with_paths(
    #     f"{MTDDH_EXTRACTED_LOCATION}/Dataset1/Regions/Test"
    # )
    # train_reg = list_files_with_paths(
    #     f"{MTDDH_EXTRACTED_LOCATION}/Dataset1/Regions/Train"
    # )
    # val_reg = list_files_with_paths(
    #     f"{MTDDH_EXTRACTED_LOCATION}/Dataset1/Regions/Validation"
    # )

    # Combine all Dataset1 mappings
    dataset1_map = {}
    for file_dict in [train_key, val_key]:
        dataset1_map.update(file_dict)
    # for file_dict in [test_reg, train_reg, val_reg]:
    #     for base_name, path in file_dict.items():
    #         if base_name not in dataset1_map:
    #             dataset1_map[base_name] = path

    # Load JSON files for dataset1
    json_files_dataset1 = [
        f"{MTDDH_EXTRACTED_LOCATION}/Dataset1/Keypoints/Keypoints_Validation.json",
        f"{MTDDH_EXTRACTED_LOCATION}/Dataset1/Keypoints/Keypoints_Train.json",
    ]
    json_base_names_dataset1 = load_json_files(json_files_dataset1)

    process_dataset(
        "dataset1", dataset1_map, data_dir, json_base_names_dataset1
    )

    dataset2_map = list_dataset2_files(
        f"{MTDDH_EXTRACTED_LOCATION}/Dataset2/png"
    )

    process_dataset("dataset2", dataset2_map, data_dir)


if __name__ == "__main__":
    main()
