from extac.mask import get_values_for_roi
from extac import utils
from extac import io
from pathlib import Path
from tqdm import tqdm
import concurrent.futures


def process_single_roi(roi, image_data, mask_data, measures, dynamic):
    """
    Process a single ROI and return the results.
    """
    data_roi = []
    for measure in measures:
        measure_func = utils._get_measure_func(measure)
        roi_values = get_values_for_roi(image_data, mask_data, roi["index"], dynamic=dynamic, measure_func=measure_func)
        data_roi.extend(
            [
                {
                    "frame": t,
                    "roi": roi["name"],
                    "measure": measure,
                    "value": val,
                }
                for t, val in enumerate(roi_values)
            ]
        )
    return data_roi


def process_rois(image_data, mask_data, rois, measures, dynamic=False, max_workers=1):
    """
    Process ROIs and extract specified measures.

    Parameters:
    -----------
    image_data : ndarray
        Image data array.
    mask_data : ndarray
        Resampled mask data array.
    rois : list
        List of ROI definitions.
    measures : list
        List of measures to extract.
    dynamic : bool, optional
        Dynamic processing flag.
    max_workers : int, optional
        Maximum number of workers for parallel processing. Defaults to 1.

    Returns:
    --------
    list
        Processed data in a long format.
    """
    # print message Provessing n ROIs with m measures in dynamic mode
    print(
        f"Processing {len(rois)} ROIs with {len(measures)} measures in {'dynamic' if dynamic else 'static'} mode with {max_workers} workers"
    )

    data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use tqdm to track progress while using map
        future_to_roi = {
            executor.submit(process_single_roi, roi, image_data, mask_data, measures, dynamic): roi for roi in rois
        }
        with tqdm(total=len(rois), desc="Processing ROIs", unit="ROI") as pbar:
            for future in concurrent.futures.as_completed(future_to_roi):
                data_roi = future.result()
                data.extend(data_roi)
                pbar.update()  # Update the progress bar for each completed ROI

    return data


def extract_tacs(
    image_file: Path,
    mask_file: Path,
    roi_file: Path,
    output_file: Path,
    measures: list = ["mean", "median", "std"],
    dynamic: bool = False,
    acquision_information_file: Path = None,
    max_workers: int = 1,
):
    """
    Wrapper function for file handling and delegating ROI extraction tasks.

    Parameters:
    -----------
    image_file : Path
        Path to image file.
    mask_file : Path
        Path to mask file.
    roi_file : Path
        Path to ROI definition file.
    output_file : Path
        Output TSV file path.
    measures : list, optional
        List of measures to extract. Default is ["mean", "median", "std"].
    dynamic : bool, optional
        Dynamic processing flag.
    acquision_information_file : Path, optional
        Path to json sidecar that contains the frame timing information. Should follow BIDS notation.
        If this is provided, addiinformation such as FrameTimeStart, FrameDuration will be added.
    max_workers : int, optional
        Maximum number of workers for parallel processing. Defaults to 1.
    """
    # Load files
    image = io.load_image(image_file)
    mask = io.load_image(mask_file)
    rois = io.read_js(roi_file)
    if acquision_information_file is not None:
        acqusisition_data = io.read_js(acquision_information_file)

    # Resample and get data
    mask_resampled = utils.resample_from_to(mask, image)
    image_data = utils.get_nibimage_data(image)
    mask_data = utils.get_nibimage_data(mask_resampled)

    # Delegate processing
    data = process_rois(image_data, mask_data, rois, measures, dynamic=dynamic, max_workers=max_workers)

    # Convert data to DataFrame
    df_pivoted = utils.pivot_and_sort_data(data)

    # add additional data if available
    if acquision_information_file is not None:
        df_pivoted = utils.add_acquisition_information(df_pivoted, acqusisition_data)

    # Save data
    io.write_tsv(df_pivoted, output_file)
