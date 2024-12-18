import numpy as np
from typing import Callable


def _create_roi_mask_from_indices(original_mask, roi_indices):
    roi_mask = np.zeros(original_mask.shape, dtype=bool)
    roi_mask[np.isin(original_mask, roi_indices)] = True

    return roi_mask


def _get_values_in_roi(roi: np.array, image: np.array) -> np.array:
    roi_values = image[roi]
    return roi_values


def _get_measure_from(masked_values: np.array, measure_func: Callable) -> float:
    if len(masked_values) == 0:
        return np.nan
    else:
        return measure_func(masked_values)


def _get_measure_from_roi_mask(image: np.array, roi: np.array, measure_func: Callable) -> float:
    roi_values = _get_values_in_roi(roi, image)
    return _get_measure_from(roi_values, np.median)


def _get_tac_from_roi_mask(dynamic_image: np.array, roi_mask: np.array, measure_func: Callable) -> np.array:
    n_frames = dynamic_image.shape[-1]
    tac = np.zeros(n_frames)
    for i, frame in enumerate(np.moveaxis(dynamic_image, -1, 0)):
        tac[i] = _get_measure_from_roi_mask(frame, roi_mask, measure_func)
    return tac


def get_tac_from_roi(image: np.array, mask: np.array, index: list, measure_func: Callable) -> np.array:
    roi_mask = _create_roi_mask_from_indices(mask, index)
    roi_tac = _get_tac_from_roi_mask(image, roi_mask, measure_func)
    return roi_tac


def get_measure_from_roi(image: np.array, mask: np.array, index: list, measure_func: Callable) -> float:
    roi_mask = _create_roi_mask_from_indices(mask, index)
    roi_mean = _get_measure_from_roi_mask(image, roi_mask, measure_func)
    return roi_mean


def get_values_for_roi(
    image: np.array,
    mask: np.array,
    roi_indices: list,
    dynamic: bool = False,
    measure_func: Callable = np.mean,
) -> np.array:
    """Convenient function to get values for a region of interest.

    Parameters
    ----------
    image : np.array
        The image data.
    mask : np.array
        The mask data.
    roi_indices : list
        The indices of the region of interest.
    measure : str
        The measure to extract.
    dynamic : bool, optional
        If True, extract TACs. If False, extract mean values, by default False
    measure_func : Callable, optional
        The function to calculate the measure, by default np.mean

    Returns
    -------
    np.array
        The values for the region of interest.
    """
    if dynamic:
        values = get_tac_from_roi(image, mask, roi_indices, measure_func)
    else:
        values = get_measure_from_roi(image, mask, roi_indices, measure_func)

    return values
