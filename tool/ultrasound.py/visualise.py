import json
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np


def load_metadata(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    info = data.get("row_data", {})
    side = data.get("side", "")
    return info, side


def overlay_mask(img, mask, alpha=0.5):
    """
    Overlay an RGB mask onto an image. Resizes mask if needed.
    """
    if len(img.shape) == 2:  # grayscale image
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # --- Ensure same spatial size ---
    if mask.shape[:2] != img.shape[:2]:
        mask = cv2.resize(
            mask, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST
        )

    # --- Prepare for blending ---
    mask_f = mask.astype(np.float32) / 255.0
    img_f = img.astype(np.float32) / 255.0
    blended = cv2.addWeighted(img_f, 1 - alpha, mask_f, alpha, 0)

    return (blended * 255).astype(np.uint8)


def visualize_ultrasound(
    image_path, mask_path, json_path=None, save_path=None
):
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path)

    if image is None or mask is None:
        raise FileNotFoundError(f"Could not read {image_path} or {mask_path}")

    meta_text = ""
    if json_path and os.path.exists(json_path):
        meta, side = load_metadata(json_path)
        meta_text = f"{side.upper()} side\n"
        for k, v in meta.items():
            if v not in [None, "NaN", np.nan]:
                meta_text += f"{k}: {v}\n"

    blended = overlay_mask(image, mask, alpha=0.4)

    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    if meta_text:
        plt.gcf().text(
            0.01,
            0.99,
            meta_text,
            fontsize=9,
            va="top",
            ha="left",
            family="monospace",
        )

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", pad_inches=0)
    plt.show()


if __name__ == "__main__":
    base_dir = "./radiopedia_ultrasound_2d/data"
    sample_id = "167854_0"

    img_path = os.path.join(base_dir, f"{sample_id}.png")
    mask_path = os.path.join(base_dir, f"{sample_id}_label.png")
    json_path = os.path.join(base_dir, f"{sample_id}.json")

    visualize_ultrasound(img_path, mask_path, json_path)
