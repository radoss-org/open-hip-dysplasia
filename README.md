# The Open Hip Dysplasia Dataset

[![DOI](https://zenodo.org/badge/955042700.svg)](https://doi.org/10.5281/zenodo.15086603)

A collection of DDH Datasets from across the Internet to help researchers and developers in the field of hip dysplasia.

<table>
  <tr>
    <td><img src="radiopedia_ultrasound_2d/data/167854_1.png" alt="DDH Radiopedia" width="300"></td>
    <td><img src="mtddh_xray_2d/data/dataset1_train_a16.jpg" alt="DDH MTDDH" width="300"></td>
    <td><img src="av_ddh_xray/raw/1116569.jpg" alt="DDH AV-DDH" width="300"></td>
    <td><img src="docs/metadata.png" alt="DDH Radiopedia" width="300"></td>
  </tr>
</table>

Currently, the dataset includes Hip Images from 4 Sources, with both X-Ray and 2D Ultrasound:
- **Radiopedia**: with information on Graf Type, Alpha Angle, Coverage, Segmentations and relavent metadata. **Released on [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode)**
- **Hong Kong Polytechnic University**: with specific information on scan quality. **Released on [Apache V2](https://www.apache.org/licenses/LICENSE-2.0)**
- **MTDDH**: A 2000+ image dataset of X-Ray images of the hip, with 8 landmarks for Acetabular Index and Wilberg Angle, as well as IHDI & Tonnis Grades. **Released on [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)**
- **[AV-DDH](av_ddh_xray/README.md)**: 2,417 raw hip X-rays with manual acetabular-index and DDH metadata. **Released on [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)**

## Data Snapshots

We use data snapshots to highlight important features of the datasets. They can be found in the README.md files of each dataset.

![MTDDH X-Ray Data Snapshot](docs/mtddh_snapshot.png)
![Radiopedia Data Snapshot](docs/radiopedia_snapshot.png)
![AV-DDH X-Ray Data Snapshot](docs/av_ddh_snapshot.png)

## Other Datasets

We also want to recognize the work of other labs who have created datasets that are not yet in this collection:
- [A dataset of DDH x-ray images](https://data.mendeley.com/datasets/jf3pv98m9g/2) - The dataset used in the relevant research article included 354 subjects (120 DDH, 234 normal) . **Released on [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)**

[The NIDUS Lab](https://nidusai.ca) has commited to enriching and simplifying Hip Datasets where possible, and adding their own datasets to the collection in the future.

## The "Open Hip" Pledge

**_To address the significant scarcity of data for AI-driven advancements in Developmental Dysplasia of the Hip (DDH), we pledge to make the Open Hip Dysplasia Dataset a robust and reliable resource. We will actively contribute new files across various modalities, including X-Ray, 3D, and 2D Sweep Videos, while simultaneously enhancing the quality of current data to maximize its utility for AI training and research. This will guarantee that anyone, regardless of their background, can access the data they need to make a meaningful impact in the field of Hip Dysplasia._**

### Sign the Pledge

If you would like to sign the pledge, please submit a pull request with your name and affiliation.

1. [RadOSS](https://github.com/radoss-org), San Francisco, California, USA
2. [The NIDUS Lab](https://nidusai.ca), University of Alberta, Edmonton, Canada


# Dataset Information

* [Radiopedia](radiopedia_ultrasound_2d/README.md) - Licence: [CC BY-NC-SA 3.0](radiopedia_ultrasound_2d/LICENSE)
* [Hong Kong Polytechnic University](hong_kong_poly_ultrasound_2d/README.md) - Licence: [Apache V2](hong_kong_poly_ultrasound_2d/LICENSE)
* [MTDDH](mtddh_xray_2d/README.md) - Licence: [CC BY 4.0](mtddh_xray_2d/LICENSE)
* [AV-DDH](av_ddh_xray/README.md) - Licence: [CC BY 4.0](av_ddh_xray/LICENSE)


# Citation

Please cite each source dataset individually using the citation information in
that dataset's README. Radiopaedia cases should be cited individually; their
case-level citations and DOIs are listed in the
[Radiopaedia README](radiopedia_ultrasound_2d/README.md).

If you cite the Open Hip Dysplasia Dataset itself, use:

```
@dataset{openhipdysplasia,
  author = {McArthur, Adam and Jaremko, Jacob L. and Hareendranathan, Abhilash and Burnside, Stephen and Kirby, Andrew and Scammon, Alexander and Sol, Damian},
  title = {The Open Hip Dysplasia Dataset},
  month = {March},
  year = {2025},
  version = {v1.0},
  doi = {10.5281/zenodo.15086603},
  url = {https://github.com/radoss-org/open-hip-dysplasia},
  note = {Adam McArthur: University of Alberta;
          Jacob L. Jaremko: University of Alberta;
          Abhilash Hareendranathan: University of Alberta;
          Stephen Burnside: University of Alberta;
          Andrew Kirby: NHS Lothian;
          Alexander Scammon: Insight Softmax Consulting;
          Damian Sol: Insight Softmax Consulting;}
}
```
