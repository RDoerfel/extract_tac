from extac.mask import get_values_for_roi
from extac import utils
from extac import io
from pathlib import Path


def extract_tacs(
    image_file: Path,
    mask_file: Path,
    roi_file: Path,
    output_file: Path,
    measures: list = ["mean", "median", "std"],
    dynamic: bool = False,
    max_workers: int = None,
):
    """
    Parallelize ROI extraction with optional worker count specification

    Parameters:
    -----------
    image_file : str
        Path to image file
    mask_file : str
        Path to mask file
    roi_file : str
        Path to ROI definition file
    output_file : str
        Output TSV file path
    measures : list, optional
        List of measures to extract. Default is ["mean", "median", "std"]
    dynamic : bool, optional
        Dynamic processing flag
    """
    # Load initial data (these remain the same for all ROIs)
    image = io.load_image(image_file)
    mask = io.load_image(mask_file)
    rois = io.read_js(roi_file)
    mask_resampled = utils.resample_from_to(mask, image)
    image_data = utils.get_nibimage_data(image)
    mask_data = utils.get_nibimage_data(mask_resampled)
    extracted_values = {}
    for roi in rois:
        for measure in measures:
            measure_func = utils._get_measure_func(measure)
            roi_values = get_values_for_roi(
                image_data, mask_data, roi["index"], dynamic=dynamic, measure_func=measure_func
            )
            extracted_values[f"{roi['name']}_{measure}"] = roi_values

    results = utils.convert_dict_to_df(extracted_values)
    io.write_tsv(results, output_file)
