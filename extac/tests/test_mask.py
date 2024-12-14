from extac.mask import create_roi_mask_from_indices
from extac.mask import _get_values_in_roi
from extac.mask import _get_mean_from
from extac.mask import get_mean_from_roi
from extac.mask import get_tac_from_roi
import numpy as np


def test_create_mask_from_indices():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = [1, 2, 3]
    mask = create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[True, True, True], [False, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [2, 3, 4]
    mask = create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, True, True], [True, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [5, 6, 7]
    mask = create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, True, True], [True, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)

    roi_indices = [8, 9]
    mask = create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, False, False], [False, True, True]])
    np.testing.assert_array_equal(mask, expected_mask)


def test_create_mask_from_indices_empty():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = []
    mask = create_roi_mask_from_indices(original_mask, roi_indices)
    expected_mask = np.array([[False, False, False], [False, False, False], [False, False, False]])
    np.testing.assert_array_equal(mask, expected_mask)


def test_create_mask_from_indices_no_match():
    original_mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_indices = [10, 11, 12]
    mask = create_roi_mask_from_indices(original_mask, roi_indices)
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


def test_get_mean_from_roi():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [1, 4, 7]
    roi = create_roi_mask_from_indices(mask, roi_index)
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_mean = get_mean_from_roi(image, roi)
    expected_roi_mean = np.array([1, 4, 7]).mean()
    assert roi_mean == expected_roi_mean


def test_get_mean_from_roi_empty():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = []
    roi = create_roi_mask_from_indices(mask, roi_index)
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_mean = get_mean_from_roi(image, roi)
    assert np.isnan(roi_mean)


def test_get_mean_from_roi_no_match():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [10, 11, 12]
    roi = create_roi_mask_from_indices(mask, roi_index)
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_mean = get_mean_from_roi(image, roi)
    assert np.isnan(roi_mean)


def test_get_tac_from_roi():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [1]
    roi = create_roi_mask_from_indices(mask, roi_index)
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = get_tac_from_roi(image, roi)
    expected_tac = np.array([1, 1, 1, 1, 1])
    np.testing.assert_array_equal(tac, expected_tac)


def test_get_tac_from_roi_mean():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [1, 2, 3]
    roi = create_roi_mask_from_indices(mask, roi_index)
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = get_tac_from_roi(image, roi)
    expected_tac = np.array([2, 2, 2, 2, 2])
    np.testing.assert_array_equal(tac, expected_tac)


def test_get_tac_from_roi_empty():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = []
    roi = create_roi_mask_from_indices(mask, roi_index)
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = get_tac_from_roi(image, roi)
    expected_tac = np.array(np.nan * 5)
    np.testing.assert_array_equal(tac, expected_tac)


def test_get_tac_from_roi_no_match():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [10, 11, 12]
    roi = create_roi_mask_from_indices(mask, roi_index)
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = get_tac_from_roi(image, roi)
    expected_tac = np.array(np.nan * 5)
    np.testing.assert_array_equal(tac, expected_tac)
