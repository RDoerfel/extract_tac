import numpy as np


def create_roi_mask_from_indices(original_mask, roi_indices):
    """
    Create a boolean mask of the same shape as the original array,
    with True where values are in the list, False otherwise.

    Parameters:
    -----------
    original_mask : numpy.ndarray
        The original array to create the mask from
    roi_indices : list
        List of integer values to match

    Returns:
    --------
    numpy.ndarray
        Boolean mask with the same shape as original_array
    """
    # Create a mask initialized with False
    roi_mask = np.zeros(original_mask.shape, dtype=bool)

    # Set True for elements that are in the value list
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


def get_mean_from_roi_mask(image: np.array, roi: np.array) -> float:
    """
    Get the mean value of the image within the ROI mask.
    Parameters
    ----------
    image : np.array
        The image data
    roi : np.array
        The mask of the ROI
    Returns
    -------
    float
        The mean value in the ROI
    """
    roi_values = _get_values_in_roi(roi, image)
    roi_mean = _get_mean_from(roi_values)
    return roi_mean


def get_tac_from_roi_mask(dynamic_image: np.array, roi_mask: np.array) -> np.array:
    """
    Extract the time activity curve (TAC) from a dynamic image in a given ROI mask.
    Parameters
    ----------
    dynamic_image : np.array
        The dynamic image data
    roi_mask : np.array
        The mask of the ROI
    Returns
    -------
    np.array
        The TAC
    """
    n_frames = dynamic_image.shape[-1]
    tac = np.zeros(n_frames)
    for i, frame in enumerate(np.moveaxis(dynamic_image, -1, 0)):
        tac[i] = get_mean_from_roi_mask(frame, roi_mask)
    return tac
