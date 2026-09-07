# Radiopedia Ultrasound 2D

## Radiopedia DataSet

Graf Class as defined by https://radiopaedia.org/articles/graf-method-for-ultrasound-classification-of-developmental-dysplasia-of-the-hip

Expect some mistakes with the side label, it was done by Qwen and I'm not sure if it's correct.

![Radiopedia Ultrasound Dataset Snapshot](../docs/radiopedia_snapshot.png)

### Licence

The data is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, see https://radiopaedia.org/licence or https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode

### File Format

Files take the form 000000-X. 000000 is the patient ID, and X is the image number. Please use the json files for more useful information.

**The length of the patient ID and image number may vary.**

### Segmentations

Segmentations are available in the `data` directory.

They are in the format of `000000-X_label.png`.

### Data Point Descriptions

*   `rad_id`: This is the unique identifier for the radiology study or examination.

*   `row_data`: This section contains the actual data extracted from the radiology report.
    *   `RadID`: Redundant identifier, same as `rad_id`.
    *   `Gender`: The patient's gender (F/M).
    *   `Age`: The patient's age at the time of the examination.  Important for DDH assessment as hip development changes rapidly in infancy.
    *   `Breech?`: Indicates whether the baby was born in breech position.  Breech birth is a risk factor for DDH.
    *   `R Graf Type`: Graf classification of the right hip.  This is a grading system for hip dysplasia based on ultrasound findings.
    *   `L Graf Type`:  Graf classification of the left hip.
    *   `R Alpha Angle`: Alpha angle measurement (in degrees) on the right hip.  This angle is formed between the ilium and the acetabular roof on ultrasound.  It is a key measurement in the Graf method.
    *   `R Beta Angle`: Beta angle measurement (in degrees) on the right hip.
    *   `L Alpha Angle`: lpha angle measurement (in degrees) on the left hip.
    *   `L Beta Angle`: Beta angle measurement (in degrees) on the left hip.
    *   `R Coverage`: Percentage of femoral head coverage by the acetabulum on the right hip.
    *   `L Coverage`: Percentage of femoral head coverage by the acetabulum on the left hip.
    *   `Notes`: Any additional notes or comments from the radiologist.
    *   `Confidence`: "Diagnosis Almost Certain" -  The radiologist's level of confidence in their diagnosis.

*   `filename`: The name of the image file associated with this data.

*   `side`: Indicates that this data refers to the left hip.


### Attribution

Attribution is tied to the number in the file name.

The DICOMs and NIFTIs use the same pattern to keep attribution clear.

### Case Citations

Each scan has an individual BibTeX citation. The `note` field identifies the
corresponding local image file.

```bibtex
@misc{radiopaedia_72628,
  author = {Sheikh, Yusra},
  title = {Developmental dysplasia of the hip - Graf type IV},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-72628},
  url = {https://radiopaedia.org/cases/72628},
  note = {Accessed on 11 Jun 2026; image: 72628_X.png}
}

@misc{radiopaedia_172535,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 2-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-172535},
  url = {https://radiopaedia.org/cases/172535},
  note = {Accessed on 11 Jun 2026; image: 172535_X.png}
}

@misc{radiopaedia_172536,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 2-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-172536},
  url = {https://radiopaedia.org/cases/172536},
  note = {Accessed on 11 Jun 2026; image: 172536_X.png}
}

@misc{radiopaedia_172658,
  author = {Thibodeau, Ryan},
  title = {Developmental dysplasia of the hip},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-172658},
  url = {https://radiopaedia.org/cases/172658},
  note = {Accessed on 11 Jun 2026; image: 172658_X.png}
}

@misc{radiopaedia_172534,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 2-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-172534},
  url = {https://radiopaedia.org/cases/172534},
  note = {Accessed on 11 Jun 2026; image: 172534_X.png}
}

@misc{radiopaedia_171555,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 1-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-171555},
  url = {https://radiopaedia.org/cases/171555},
  note = {Accessed on 11 Jun 2026; image: 171555_X.png}
}

@misc{radiopaedia_171556,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 4-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-171556},
  url = {https://radiopaedia.org/cases/171556},
  note = {Accessed on 11 Jun 2026; image: 171556_X.png}
}

@misc{radiopaedia_172533,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 1-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-172533},
  url = {https://radiopaedia.org/cases/172533},
  note = {Accessed on 11 Jun 2026; image: 172533_X.png}
}

@misc{radiopaedia_171551,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 4-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-171551},
  url = {https://radiopaedia.org/cases/171551},
  note = {Accessed on 11 Jun 2026; image: 171551_X.png}
}

@misc{radiopaedia_171553,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 1-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-171553},
  url = {https://radiopaedia.org/cases/171553},
  note = {Accessed on 11 Jun 2026; image: 171553_X.png}
}

@misc{radiopaedia_171554,
  author = {Thibodeau, Ryan},
  title = {Normal hip ultrasound - 2-month-old},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-171554},
  url = {https://radiopaedia.org/cases/171554},
  note = {Accessed on 11 Jun 2026; image: 171554_X.png}
}

@misc{radiopaedia_167854,
  author = {Ranchod, Ashesh Ishwarlal},
  title = {Developmental dysplasia of the hip - Graf type IIa},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-167854},
  url = {https://radiopaedia.org/cases/167854},
  note = {Accessed on 11 Jun 2026; image: 167854_X.png}
}

@misc{radiopaedia_167855,
  author = {Ranchod, Ashesh Ishwarlal},
  title = {Developmental dysplasia of the hip - Graf type Ib},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-167855},
  url = {https://radiopaedia.org/cases/167855},
  note = {Accessed on 11 Jun 2026; image: 167855_X.png}
}

@misc{radiopaedia_167857,
  author = {Ranchod, Ashesh Ishwarlal},
  title = {Developmental dysplasia of the hip - Graf type Ia},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-167857},
  url = {https://radiopaedia.org/cases/167857},
  note = {Accessed on 11 Jun 2026; image: 167857_X.png}
}

@misc{radiopaedia_56568,
  author = {Alwakkaa, Hisham},
  title = {Developmental dysplasia of the hips - bilateral Graf type IIa},
  howpublished = {Case study, Radiopaedia.org},
  doi = {10.53347/rID-56568},
  url = {https://radiopaedia.org/cases/56568},
  note = {Accessed on 11 Jun 2026; image: 56568_X.png}
}
```

### Attribution Format

Case courtesy of Name from https://radiopaedia.org rID [Radiopaedia ID] (https://radiopaedia.org/cases/rID)
