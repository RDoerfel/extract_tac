import numpy as np
import nibabel as nib
from nilearn.image import resample_to_img
import pandas as pd


def resample_from_to(image_from: nib.Nifti1Image, image_to: nib.Nifti1Image) -> nib.Nifti1Image:
    return resample_to_img(image_from, image_to, interpolation="nearest", copy_header=True)


def get_nibimage_data(nibimage: nib.Nifti1Image) -> np.array:
    return nibimage.get_fdata()


def convert_list_of_dicts_to_dataframe(list_of_dicts: list) -> pd.DataFrame:
    return pd.DataFrame({k: v for d in list_of_dicts for k, v in d.items()})
