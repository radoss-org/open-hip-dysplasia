# AV-DDH X-Ray

This directory contains the files used from version 2 of the
[Acetabular-vision hip developmental dysplasia (AV-DDH) dataset](https://data.mendeley.com/datasets/4gvcb6gmh2/2)
([DOI: 10.17632/4gvcb6gmh2.2](https://doi.org/10.17632/4gvcb6gmh2.2)).

## Included files

- `raw/`: 2,417 original X-ray images (2,276 JPG and 141 PNG files)
- `data.xlsx`: 2,417 matching metadata rows
- `LICENSE`: the source dataset's CC BY 4.0 license

The Roboflow `yolov8/` export and the source ZIP archives are not included, due to the pre-augmented images not being available. They can be found here: https://data.mendeley.com/datasets/4gvcb6gmh2/2

## Snapshot

Generate the snapshot from `env/open-hip-dysplasia` with:

```bash
python tool/create_av_ddh_snapshot.py
```

![AV-DDH data snapshot](../docs/av_ddh_snapshot.png)

## Attribution and license

AV-DDH was published by Bassem Haddad and co-authors on Mendeley Data. The
source record describes 2,417 raw X-ray images with associated annotations and
metadata. The included source files are provided under the
[Creative Commons Attribution 4.0 International license](LICENSE).

## Citation

```bibtex
@dataset{haddad2026avddh,
  author    = {Haddad, Bassem and AlHosanie, Tasneem and Dweidari, Ahmed and
               Mahmoud, Hasan and AbuAmouneh, Nora and AlNatsheh, Tala and
               Mazahreh, Leen and Abdallah, Amr and Kanaan, Ali and Abdallat,
               Bdour and Younis, Ahmad and Haddad, Sand and Khalaf, Hamza and
               Aldowekat, Osama and Atiani, Serin and Ali, Hakam and Bshoukhoj,
               Shamel and Banihani, Rand and Alhijawi, Bushra},
  title     = {Acetabular-vision hip developmental dysplasia's (AV-DDH)},
  year      = {2026},
  publisher = {Mendeley Data},
  version   = {V2},
  doi       = {10.17632/4gvcb6gmh2.2}
}
```
