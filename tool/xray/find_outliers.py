import json
import os
from pathlib import Path

KNOWN_OUTLIERS = {
    "Old": ["dataset2_90d75cba_img", "dataset2_3415d946_img"],
    "Wrong Body Part": [
        "dataset2_306feb9a_img",
        "dataset2_e977cf36_img",
        "dataset2_f68ab7a6_img",
        "dataset2_8dd741ed_img",
        "dataset2_e977cf36_img",
        "dataset2_6d4ff308_img",
        "dataset2_f3e8f7f8_img",
        "dataset2_5bb4943f_img",
        "dataset2_bcbec32d_img",
        "dataset2_aecbeb0b_img",
        "dataset2_b20e2247_img",
        "dataset2_fbdae91f_img",
        "dataset2_fbdae91f_img",
    ],
    "Label Points Wrong Way Round": [
        "dataset1_train_h81",
        "dataset2_95481ad2_img",
        "dataset2_6449bb8d_img",
        "dataset1_train_y3",
    ],
}

FALSE_NEGATIVES = [
    "dataset1_train_y3",
    "dataset1_train_y44",
    "dataset2_6b8b2988_img",
    "dataset2_9461a9ba_img",
    "dataset2_b67c3a4d_img",
]


def load_yolo_pose_label(label_path):
    poses = []
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            cls = int(parts[0])
            xc, yc, w, h = map(float, parts[1:5])
            keypoints = []
            for i in range(5, len(parts), 3):
                try:
                    xk = float(parts[i])
                    yk = float(parts[i + 1])
                    vk = int(float(parts[i + 2]))
                    keypoints.append((xk, yk, vk))
                except IndexError:
                    break
            poses.append((cls, xc, yc, w, h, keypoints))
    return poses


def is_pose_horizontal(poses):
    """Return True if any class-1 object is more horizontal than vertical."""
    for cls, xc, yc, w, h, kpts in poses:
        if cls != 1:
            continue

        xs = [x for x, y, v in kpts if v > 0]
        ys = [y for x, y, v in kpts if v > 0]

        if len(xs) < 2 or len(ys) < 2:
            continue

        x_range = max(xs) - min(xs)
        y_range = max(ys) - min(ys)

        if x_range > y_range:
            return True
    return False


def get_existing_image_path(image_stem, data_dir):
    """Return the image path (preferring .jpg, then .png) or None if missing."""
    jpg_path = data_dir / f"{image_stem}.jpg"
    png_path = data_dir / f"{image_stem}.png"

    if jpg_path.exists():
        return str(jpg_path)
    elif png_path.exists():
        return str(png_path)
    else:
        return None


def find_non_ap_pelvis(data_dir):
    """Scan all .txt labels in data_dir and return dictionary with results."""
    data_dir = Path(data_dir)
    txt_files = sorted(data_dir.glob("*.txt"))
    horizontal_files = []
    h_files_not_horizontal = []
    missing_files = []

    for label_file in txt_files:
        poses = load_yolo_pose_label(label_file)
        if is_pose_horizontal(poses) and not any(
            fn in str(label_file.stem) for fn in FALSE_NEGATIVES
        ):
            horizontal_files.append(label_file.stem)
        elif "_h" in str(label_file):
            h_files_not_horizontal.append(label_file.stem)

    result = {"Known Frog-Leg Views": [], "Missing": []}

    for f in horizontal_files:
        img_path = get_existing_image_path(f, data_dir)
        if img_path:
            result["Known Frog-Leg Views"].append(f)
        else:
            missing_files.append(f)

    for reason, image_list in KNOWN_OUTLIERS.items():
        result[reason] = []
        for stem in image_list:
            img_path = get_existing_image_path(stem, data_dir)
            if img_path:
                result[reason].append(stem)
            else:
                missing_files.append(stem)

    result["Missing"] = sorted(set(missing_files))

    return result


if __name__ == "__main__":
    data_dir = "./mtddh_xray_2d/data"
    out_json_path = Path("outliers.json")

    results = find_non_ap_pelvis(data_dir)

    with open(out_json_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Outliers written to {out_json_path.resolve()}")
