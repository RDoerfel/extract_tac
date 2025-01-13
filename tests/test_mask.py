from extac.mask import _create_roi_mask_from_indices
from extac.mask import _get_values_in_roi
from extac.mask import _get_measure_from
from extac.mask import _get_measure_from_roi_mask
from extac.mask import _get_tac_from_roi_mask
from extac.mask import get_measure_from_roi
from extac.mask import get_tac_from_roi
from extac.mask import get_values_for_roi
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
    roi_mean = _get_measure_from(masked_image, np.mean)
    expected_roi_mean = masked_image.mean()
    assert roi_mean == expected_roi_mean

    masked_image = np.array([0, 0])
    roi_mean = _get_measure_from(masked_image, np.mean)
    expected_roi_mean = masked_image.mean()
    assert roi_mean == expected_roi_mean


def test_get_measure_from_roi_mask_mean():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [1, 4, 7]
    roi = _create_roi_mask_from_indices(mask, roi_index)
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_mean = _get_measure_from_roi_mask(image, roi, np.mean)
    expected_roi_mean = np.array([1, 4, 7]).mean()
    assert roi_mean == expected_roi_mean


def test_get_measure_from_roi_mask_empty_mean():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = []
    roi = _create_roi_mask_from_indices(mask, roi_index)
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_mean = _get_measure_from_roi_mask(image, roi, np.mean)
    assert np.isnan(roi_mean)


def test_get_measure_from_roi_mask_no_match():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [10, 11, 12]
    roi = _create_roi_mask_from_indices(mask, roi_index)
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_mean = _get_measure_from_roi_mask(image, roi, np.mean)
    assert np.isnan(roi_mean)


def test_get_tac_from_roi_mask():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [1]
    roi = _create_roi_mask_from_indices(mask, roi_index)
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = _get_tac_from_roi_mask(image, roi, np.mean)
    expected_tac = np.array([1, 1, 1, 1, 1])
    np.testing.assert_array_equal(tac, expected_tac)


def test_get_tac_from_roi_mask_mean():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [1, 2, 3]
    roi = _create_roi_mask_from_indices(mask, roi_index)
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = _get_tac_from_roi_mask(image, roi, np.mean)
    expected_tac = np.array([2, 2, 2, 2, 2])
    np.testing.assert_array_equal(tac, expected_tac)


def test_get_tac_from_roi_mask_empty():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = []
    roi = _create_roi_mask_from_indices(mask, roi_index)
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = _get_tac_from_roi_mask(image, roi, np.mean)
    expected_tac = np.array(np.nan * 5)
    np.testing.assert_array_equal(tac, expected_tac)


def test_get_tac_from_roi_mask_no_match():
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    roi_index = [10, 11, 12]
    roi = _create_roi_mask_from_indices(mask, roi_index)
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = _get_tac_from_roi_mask(image, roi, np.mean)
    expected_tac = np.array(np.nan * 5)
    np.testing.assert_array_equal(tac, expected_tac)


def test_get_mean_from_roi():
    roi_index = [1, 2, 3]
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    mean = get_measure_from_roi(image, mask, roi_index, np.mean)
    expected_mean = np.array([1, 2, 3]).mean()
    assert mean == np.array(expected_mean)


def test_get_tac_from_roi():
    roi_index = [1, 2, 3]
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    tac = get_tac_from_roi(image, mask, roi_index, np.mean)
    expected_tac = np.array([2, 2, 2, 2, 2])
    np.testing.assert_array_equal(tac, expected_tac)


def test_get_values_for_roi_static_mean():
    dynamic = False
    roi_index = [1, 2, 3]
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    values = get_values_for_roi(image, mask, roi_index, np.mean, dynamic)
    expected_values = np.array([1, 2, 3]).mean()
    assert values == expected_values


def test_get_values_for_roi_static_volume():
    dynamic = False
    roi_index = [1, 2, 3]
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    values = get_values_for_roi(image, mask, roi_index, len, dynamic)
    expected_values = len(np.array([1, 2, 3]))
    assert values == expected_values


def test_get_values_for_roi_dynamic_mean():
    dynamic = True
    roi_index = [1, 2, 3]
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    values = get_values_for_roi(image, mask, roi_index, np.mean, dynamic)
    expected_values = np.array([2, 2, 2, 2, 2])
    np.testing.assert_array_equal(values, expected_values)


def test_get_values_for_roi_dynamic_volume():
    dynamic = True
    roi_index = [1, 2, 3]
    mask = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    image = np.repeat(mask[:, :, np.newaxis], 5, axis=2)
    values = get_values_for_roi(image, mask, roi_index, len, dynamic)
    expected_values = np.array([3, 3, 3, 3, 3])
    np.testing.assert_array_equal(values, expected_values)
