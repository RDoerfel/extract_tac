import numpy as np


def _create_roi_mask_from_indices(original_mask, roi_indices):
    roi_mask = np.zeros(original_mask.shape, dtype=bool)
    roi_mask[np.isin(original_mask, roi_indices)] = True

    return roi_mask


def _get_values_in_roi(roi: np.array, image: np.array) -> np.array:
    roi_values = image[roi]
    return roi_values


def _get_mean_from(masked_values: np.array) -> float:
    if len(masked_values) == 0:
        return np.nan
    else:
        return masked_values.mean()


def _get_mean_from_roi_mask(image: np.array, roi: np.array) -> float:
    roi_values = _get_values_in_roi(roi, image)
    roi_mean = _get_mean_from(roi_values)
    return roi_mean


def _get_tac_from_roi_mask(dynamic_image: np.array, roi_mask: np.array) -> np.array:
    n_frames = dynamic_image.shape[-1]
    tac = np.zeros(n_frames)
    for i, frame in enumerate(np.moveaxis(dynamic_image, -1, 0)):
        tac[i] = _get_mean_from_roi_mask(frame, roi_mask)
    return tac


def get_mean_from_roi(image: np.array, mask: np.array, index: list) -> float:
    """Get the mean value of the image in the region of interest defined by the index.

    Parameters
    ----------
    image : np.array
        The image data.
    mask : np.array
        The mask data.

    Returns
    -------
    float
        The mean value of the image in the region of interest.
    """
    roi_mask = _create_roi_mask_from_indices(mask, index)
    roi_mean = _get_mean_from_roi_mask(image, roi_mask)
    return roi_mean


def get_tac_from_roi(image: np.array, mask: np.array, index: list):
    """Get the time activity curve of the image in the region of interest defined by the index.

    Parameters
    ----------
    image : np.array
        The image data.
    mask : np.array
        The mask data.

    Returns
    -------
    np.array
        The time activity curve of the image in the region of interest.
    """
    roi_mask = _create_roi_mask_from_indices(mask, index)
    roi_tac = _get_tac_from_roi_mask(image, roi_mask)
    return roi_tac
