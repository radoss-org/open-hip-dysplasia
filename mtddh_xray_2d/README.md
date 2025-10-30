# MTDDH Dataset

The data has been transformed into the YOLO format, and is available in the `data` directory.

You can read about the YOLO format [here](https://docs.ultralytics.com/datasets/).

All other information can be found here: https://www.nature.com/articles/s41597-025-05146-x.

## Processing

There are 1878 images total in our dataset.

| **Dataset Information** |                                  |
|--------------------------|----------------------------------|
| **Age Range**            | 5–40 months                      |
| **Sample Size**          | Dataset 1: 973 images<br>Dataset 2: 905 images |
| **Gender Ratio (F:M)**   | Dataset 1: 1.67:1 <br>Dataset 2: 1.45:1     |
| **Mean Age**             | Dataset 1: 14.57 months<br>Dataset 2: 14.32 months |
| **Median Age**           | Dataset 1: 13 months<br>Dataset 2: 12 months       |
| **Key Points**           | 8 anatomical landmarks           |

We observed that the original MTDDH dataset has 2232 images. The reasons for this discrepancy are laid out below:

### Dataset 1

We found that Dataset 1 has 1326 Images (vs the 1250 reported).

81 of them were just in the Regions dataset, not the Landmarks Dataset. This leaves 1245 (Very close to the original count)

206 of those were the Test set - where no landmark labels could be found. A further 52 images in the training/validation sets were missing labels. A further 14 were removed as their landmarks could not be extracted properly. This leaves a final count of 973 (1326-81-206-52-14=973).

### Dataset 2

We found that only one file could not be processed in Dataset 2, leaving 905 Images.

## Data Split

A further 51 were removed for failing further processing before creating the split. Both datasets were randomly split and merged together to leave 1827 images in the split.

This split can be found in `mtddh_xray_2d/dataset_splits.json`

We report 3 different types of outliers for exclusion:
- Non AP Pevlis Views (111)
- Older than 40 Months (2)
- Wrong Body Part (13)

These outliers can be found in `mtddh_xray_2d/outliers.json`

## Visualising Keypoints

We have created a simple script to

## Licence

The data is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, see https://creativecommons.org/licenses/by/4.0/.

![](../docs/mtddh_snapshot.png)