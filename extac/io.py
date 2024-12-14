from pathlib import Path
import nibabel as nib
import pandas as pd
import json as js


def load_image(image_path: Path) -> nib.Nifti1Image:
    return nib.load(image_path)


def read_js(js_file: Path):
    with open(js_file, "r") as f:
        rois = js.load(f)
    return rois


def write_tsv(df: pd.DataFrame, tsv_path: Path):
    df.to_csv(tsv_path, sep="\t", index=False)
