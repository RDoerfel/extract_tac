from extac.mask import get_values_for_roi
from extac import utils
from extac import io
from pathlib import Path


def extract_tacs(image_file: Path, mask_file: Path, roi_file: Path, output_file: Path, dynamic: bool = True):
    """Extract TACs from an image using a mask and ROIs
    Parameters
    ----------
        image_file: Path
            Path to the image file
        mask_file: Path
            Path to the mask file
        roi_file: Path
            Path to the ROI file
        output_file: Path
            Path to the output file
        dynamic: bool
            If True, extract TACs. If False, extract mean values
    """

    image = io.load_image(image_file)
    mask = io.load_image(mask_file)
    rois = io.read_js(roi_file)
    mask_resampled = utils.resample_from_to(mask, image)
    image_data = utils.get_nibimage_data(image)
    mask_data = utils.get_nibimage_data(mask_resampled)
    extracted_values = []
    for roi in rois:
        roi_values = get_values_for_roi(image_data, mask_data, roi["index"], dynamic=dynamic)
        result_dict = {roi["name"]: roi_values}
        extracted_values.append(result_dict)

    results = utils.convert_list_of_dicts_to_dataframe(extracted_values)
    io.write_tsv(results, output_file)
