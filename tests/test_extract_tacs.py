import pytest
import numpy as np
from extac import extract_tacs


@pytest.fixture
def mock_data():
    """Fixture to provide mock data for testing."""
    rois = [
        {"name": "roi1", "index": 1},
        {"name": "roi2", "index": 2},
    ]

    # Static case: 2D image
    mask_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    static_image_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    dynamic_image_data = np.repeat(static_image_data[:, :, np.newaxis], 5, axis=2)  # Add time axis

    measures = ["mean", "median"]

    return {
        "static": (static_image_data, mask_data, rois, measures),
        "dynamic": (dynamic_image_data, mask_data, rois, measures),
    }


@pytest.fixture
def mock_get_values_for_roi(monkeypatch):
    """Fixture to mock `get_values_for_roi` function."""

    def mock_function(image_data, mask_data, roi_index, dynamic, measure_func):
        if dynamic:
            # Dynamic case: Return time series data
            if roi_index == 1:
                return np.array([1, 2, 3, 4, 5])  # Example values for ROI 1
            elif roi_index == 2:
                return np.array([6, 7, 8, 9, 10])  # Example values for ROI 2
        else:
            # Static case: Return a single aggregated value
            if roi_index == 1:
                return np.array([5])  # Example aggregated value for ROI 1
            elif roi_index == 2:
                return np.array([6])  # Example aggregated value for ROI 2

    monkeypatch.setattr("extac.extract_tacs.get_values_for_roi", mock_function)


def test_process_rois_static(mock_data, mock_get_values_for_roi):
    image_data, mask_data, rois, measures = mock_data["static"]

    data = extract_tacs.process_rois(image_data, mask_data, rois, measures, dynamic=False)

    # Assertions
    assert len(data) == 4  # 2 ROIs x 2 measures x 1 frame

    # Create a dictionary to easily check values
    data_dict = {(item["roi"], item["measure"]): item["value"] for item in data}

    assert data_dict[("roi1", "mean")] == 5
    assert data_dict[("roi2", "mean")] == 6
    assert data_dict[("roi1", "median")] == 5
    assert data_dict[("roi2", "median")] == 6


def test_process_rois_dynamic(mock_data, mock_get_values_for_roi):
    image_data, mask_data, rois, measures = mock_data["dynamic"]

    data = extract_tacs.process_rois(image_data, mask_data, rois, measures, dynamic=True)

    # Assertions
    assert len(data) == 20  # 2 ROIs x 2 measures x 5 frames
    assert data[0]["roi"] == "roi1"
    assert data[0]["frame"] == 0
    assert data[0]["value"] == 1
    assert data[-1]["roi"] == "roi2"
    assert data[-1]["frame"] == 4
    assert data[-1]["value"] == 10
