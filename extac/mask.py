import numpy as np


def create_mask_from_indices(original_mask, roi_indices):
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
    mask = np.zeros(original_mask.shape, dtype=bool)

    # Set True for elements that are in the value list
    mask[np.isin(original_mask, roi_indices)] = True

    return mask
