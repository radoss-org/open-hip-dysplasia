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

A further 51 were removed for failing further processing before creating the split. Both datasets were randomly split and merged together to leave 1827 images in the working set.

The working set was stratified by IHDI grade, using the higher grade from the two hips, and split at the image level into 40% training (731 images), 20% validation (365), and 40% test (731). The released files do not contain patient identifiers or visit linkage, so patient-level splitting cannot be verified.

Only the training split is oversampled for grades 2–4. The split file records the 731 original training IDs; generated YOLO training directories contain 1109 files after adding 378 oversampled copies.

This split can be found in `mtddh_xray_2d/dataset_splits.json`

The snapshot generator reads the 1827-case working-set metrics from `MTDDH_METRICS_ROOT` (default: `retuve-data/testing-manual`) and writes `docs/mtddh_snapshot.png`.

## Outliers

The outlier metadata contains:
- Known Frog-Leg Views (111)
- Old (2)
- Wrong Body Part (14)
- Label Points Wrong Way Round (3)
- Lots of Ortho Implants (1)
- Missing (0)

These cases remain in the source dataset and split files. For final internal test analysis, 52 test images were excluded: 40 frog-leg views, 10 wrong-body-part images, 1 image with reversed label points, and 1 image with extensive orthopaedic implants.

These outliers can be found in `mtddh_xray_2d/outliers.json`

## Visualising Keypoints

The snapshot script includes metric distributions, a full-name,
image-direction-aware landmark visualization, an example Retuve `.jpg` output
with its measurement lines, and a grouped Dataset 1 letter-grade versus
maximum-IHDI-grade confusion matrix. Run it from `env/open-hip-dysplasia` with:

```bash
MTDDH_METRICS_ROOT=../xray-experiments/retuve-data/testing-manual \
  python tool/create_mtddh_snapshot.py
```

The example is `dataset1_validation_h99`, a standard view with left/right IHDI
grades 1 and 4.

The confusion-matrix rows combine `b/c/w/y`, `e/h`, and `d/l/o`; `a` remains
separate.

## Licence

The data is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, see https://creativecommons.org/licenses/by/4.0/.

## Citation

```bibtex
@misc{c088644bd0b2406eb49830ad447c17fb,
  author       = {Guoqiang Qi and Xiongfei Jiao and Jing Li and Chaojin Qin and Xinxin Li and Zhexian Sun and Yonggen Zhao and Renjie Jiang and Zhu Zhu and Guoqiang Zhao and Gang Yu},
  title        = {{The MTDDH dataset for quality evaluation of pelvic X-ray and diagnosis of developmental dysplasia of the hip}},
  year         = 2025,
  month        = apr,
  publisher    = {Science Data Bank},
  version      = {V1},
  doi          = {10.57760/sciencedb.24372},
  url          = {https://doi.org/10.57760/sciencedb.24372}
}
```

![](../docs/mtddh_snapshot.png)
