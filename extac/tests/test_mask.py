from extac.mask import _create_roi_mask_from_indices
from extac.mask import _get_values_in_roi
from extac.mask import _get_mean_from
from extac.mask import extract_roi_mean
import numpy as np


def test_create_mask_from_indices():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = [1, 2, 3]
    mask = _create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[True, True, True], [False, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [2, 3, 4]
    mask = _create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, True, True], [True, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [5, 6, 7]
    mask = _create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, True, True], [True, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [8, 9]
    mask = _create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, False, False], [False, True, True]])
    np.testing.assert_array_equal(mask, expected_mask)


def test_create_mask_from_indices_empty():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = []
    mask = _create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)


def test_create_mask_from_indices_no_match():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = [10, 11, 12]
    mask = _create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)


def test_mask_image():
    mask = np.array([[True, True, True], [False, False, False], [False, False, False]])
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    masked_image = _get_values_in_roi(mask, image)
    expected_masked_image = np.array([1, 2, 3])
    np.testing.assert_array_equal(masked_image, expected_masked_image)

    mask = np.array([[False, True, True], [True, False, False], [False, False, False]])
    masked_image = _get_values_in_roi(mask, image)
    expected_masked_image = np.array([2, 3, 4])
    np.testing.assert_array_equal(masked_image, expected_masked_image)


def test_mask_image_empty():
    mask = np.array([[False, False, False], [False, False, False], [False, False, False]])
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    masked_image = _get_values_in_roi(mask, image)
    expected_masked_image = np.array([])
    np.testing.assert_array_equal(masked_image, expected_masked_image)


def test_get_mean_from():
    masked_image = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    roi_mean = _get_mean_from(masked_image)
    expected_roi_mean = masked_image.mean()
    assert roi_mean == expected_roi_mean

    masked_image = np.array([0, 0])
    roi_mean = _get_mean_from(masked_image)
    expected_roi_mean = masked_image.mean()
    assert roi_mean == expected_roi_mean


def test_extract_roi_mean():
    roi_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [1, 4, 7]
    roi_mean = extract_roi_mean(roi_mask, image, roi_index)
    expected_roi_mean = np.array([1, 4, 7]).mean()
    assert roi_mean == expected_roi_mean
