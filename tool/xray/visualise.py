import os

import cv2
import matplotlib.pyplot as plt


def load_yolo_pose_label(label_path):
    poses = []
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            cls = int(parts[0])
            xc, yc, w, h = map(float, parts[1:5])
            # Remaining values are keypoints (x, y, visibility)
            keypoints = []
            for i in range(5, len(parts), 3):
                try:
                    xk = float(parts[i])
                    yk = float(parts[i + 1])
                    vk = int(
                        float(parts[i + 2])
                    )  # sometimes "2" may be float-like
                    keypoints.append((xk, yk, vk))
                except IndexError:
                    break
            poses.append((cls, xc, yc, w, h, keypoints))
    return poses


def visualize_pose(image_path, label_path, save_path=None):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image {image_path}")
    h, w = image.shape[:2]

    poses = load_yolo_pose_label(label_path)

    for cls, xc, yc, bw, bh, keypoints in poses:
        # Compute bbox in pixel coordinates
        x1 = int((xc - bw / 2) * w)
        y1 = int((yc - bh / 2) * h)
        x2 = int((xc + bw / 2) * w)
        y2 = int((yc + bh / 2) * h)
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
            cv2.LINE_AA,
        )

        # Draw keypoints with index numbers
        for idx, (xk, yk, vk) in enumerate(keypoints):
            if vk == 0:
                continue  # not visible
            px = int(xk * w)
            py = int(yk * h)

            # NEW: keep colors for visible/invisible points
            color = (0, 0, 255) if vk == 1 else (255, 0, 0)

            cv2.circle(image, (px, py), 3, color, -1)

            # NEW: label each point by its index (starting at 0)
            cv2.putText(
                image,
                str(idx),
                (px + 5, py - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

    plt.figure(figsize=(8, 8))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight", pad_inches=0)
    plt.show()


if __name__ == "__main__":
    img_path = "./mtddh_xray_2d/data/dataset1_train_a315.jpg"
    label_path = img_path.replace(".jpg", ".txt")

    # You can include a save_path with:
    # visualize_pose(img_path, label_path, save_path="./test-xray.png")
    visualize_pose(img_path, label_path)
