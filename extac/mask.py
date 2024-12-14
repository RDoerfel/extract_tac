import numpy as np


def _create_roi_mask_from_indices(original_mask, roi_indices):
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
    roi_mean = masked_values.mean()
    return roi_mean


def extract_roi_mean(region_masks: np.array, image: np.array, roi_index: list) -> float:
    """Extract the mean value in the image within the region of interest defined by the roi_index
    Parameters:
    -----------
    region_masks : numpy.ndarray
        The mask image
    image : numpy.ndarray
        The image to extract the mean value from
    roi_index : list
        List of integer values to match

    Returns:
    --------
    float
        Mean value in the image within the region of interest
    """
    roi_mask = _create_roi_mask_from_indices(region_masks, roi_index)
    roi_values = _get_values_in_roi(roi_mask, image)
    roi_mean = _get_mean_from(roi_values)
    return roi_mean
