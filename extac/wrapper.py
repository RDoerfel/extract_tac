import numpy as np
import nibabel as nib
from extac.mask import get_tac_from_roi, get_mean_from_roi
from extac.utils import get_nibimage_data


def get_values_for_roi(
    image: nib.Nifti1Image, mask: nib.Nifti1Image, roi_indices: list, dynamic: bool = False
) -> np.array:
    image_data = get_nibimage_data(image)
    mask_data = get_nibimage_data(mask)
    if dynamic:
        values = get_tac_from_roi(image_data, mask_data, roi_indices)
    else:
        values = get_mean_from_roi(image_data, mask_data, roi_indices)

    return values
