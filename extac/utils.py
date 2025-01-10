import numpy as np
import nibabel as nib
from nilearn.image import resample_to_img
import pandas as pd
from typing import Callable


def resample_from_to(image_from: nib.Nifti1Image, image_to: nib.Nifti1Image) -> nib.Nifti1Image:
    return resample_to_img(image_from, image_to, interpolation="nearest", copy_header=True, force_resample=True)


def get_nibimage_data(nibimage: nib.Nifti1Image) -> np.array:
    return nibimage.get_fdata()


def convert_dict_to_df(dict_to_convert: dict) -> pd.DataFrame:
    return pd.DataFrame.from_dict(dict_to_convert, orient="index").T


def _get_measure_func(measure_string: str) -> Callable:
    if measure_string == "mean":
        return np.mean
    elif measure_string == "median":
        return np.median
    elif measure_string == "std":
        return np.std
    elif measure_string == "count":
        return np.count_nonzero
    else:
        raise ValueError("Invalid measure string")
    return


def pivot_and_sort_data(data):
    """
    Pivot and sort data for final output.

    Parameters:
    -----------
    data : list
        Processed data in a long format.

    Returns:
    --------
    DataFrame
        Pivoted and sorted DataFrame.
    """
    df = pd.DataFrame(data)

    # Pivot the DataFrame
    df_pivoted = df.pivot(index=["frame", "roi"], columns="measure", values="value").reset_index()

    # Flatten the multi-level columns
    df_pivoted.columns.name = None
    df_pivoted.columns = [col if isinstance(col, str) else col for col in df_pivoted.columns]

    # Sort by ROI with increasing frame
    df_pivoted = df_pivoted.sort_values(["roi", "frame"]).reset_index(drop=True)

    return df_pivoted
