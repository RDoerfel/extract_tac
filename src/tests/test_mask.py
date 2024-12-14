from src.mask import create_mask_from_indices
import numpy as np


def test_create_mask_from_indices():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = [1, 2, 3]
    mask = create_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[True, True, True], [False, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [2, 3, 4]
    mask = create_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, True, True], [True, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [5, 6, 7]
    mask = create_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, True, True], [True, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [8, 9]
    mask = create_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, False, False], [False, True, True]])
    np.testing.assert_array_equal(mask, expected_mask)


def test_create_mask_from_indices_empty():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = []
    mask = create_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)


def test_create_mask_from_indices_no_match():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = [10, 11, 12]
    mask = create_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)
