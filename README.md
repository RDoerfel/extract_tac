
# extract_tac

This is a simple tool to extract Time Activity Curves (TACs) or single values (such as mean, median, etc.) from dynamic or static image data using a segmentation mask. It allows for extracting statistics from multiple Regions of Interest (ROIs) and can handle both static and dynamic images.

## Installation

Easily install it from GitHub using `pip`:

```bash
pip install git+https://github.com/RDoerfel/extract_tac.git
```

## Command Line Interface

The tool provides a command-line interface for extracting TACs or single values from images based on specified masks and regions of interest (ROIs).

### Usage

```bash
python -m extract_tac --image <image_path> --mask <mask_path> --rois <rois_path> --output <output_path> [options]
```

### Required Arguments

- `--image`: Path to the input image file.
  - Example: `--image /path/to/pet_image.nii.gz`

- `--mask`: Path to the mask file.
  - Example: `--mask /path/to/brain_mask.nii.gz`

- `--rois`: Path to the ROIs file containing region definitions.
  - Example: `--rois /path/to/regions.json`

- `--output`: Path where the output will be saved.
  - Example: `--output /path/to/results.tsv`

### ROI Definition File Format

The ROI definition file should be in JSON format, where each ROI is defined with a name and corresponding index values. The index should correspond to values in your mask image. Here's the expected structure:

```json
[
    {
        "name": "insula",
        "index": [1035, 2035]
    },
    {
        "name": "temporal-lobe",
        "index": [
            1001, 1009, 1015, 1030, 1034,
            2001, 2009, 2015, 2030, 2034
        ]
    }
]
```

You can find example ROI definitions for Freesurfer aseg+aparc segmentations in the [examples](./bin) directory.

In general, each ROI entry contains:
- `name`: A string identifier for the region.
- `index`: An array of integer values representing the indices that define this region in the mask. For custom masks, this will typically be a single value.

### Optional Arguments

- `--measure`: Specify one or more statistical measures to extract.
  - Available options: `mean`, `median`, `std`, `count`
  - Default: All measures (`mean`, `median`, `std`, `count`)
  - Example for single measure: `--measure mean`
  - Example for multiple measures: `--measure mean std`

- `--dynamic`: Flag to extract time activity curves (TACs).
  - If present: Extracts TACs over time.
  - If absent: Extracts single values per ROI.
  - Example: `--dynamic`

- `--acquisition_information`: Path to a JSON sidecar file that contains frame timing information.
  - This file should follow the **BIDS notation** and include data such as `frame_start`, `frame_duration`, etc.
  - Example: `--acquisition_information /path/to/pet_image.json`

### Example Usage

1. **Extract mean and standard deviation from a static image:**

```bash
python -m extract_tac --image pet.nii.gz --mask brain.nii.gz --rois regions.json --output results.tsv --measure mean std
```

2. **Extract all measures and generate TACs:**

```bash
python -m extract_tac --image dynamic_pet.nii.gz --mask brain.nii.gz --rois regions.json --output tacs.tsv --dynamic
```

3. **Extract only median values from a static image:**

```bash
python -m extract_tac --image pet.nii.gz --mask brain.nii.gz --rois regions.json --output median_values.tsv --measure median
```

### Output Format

The output is saved as a.tsv file, which varies based on whether dynamic mode is enabled.

#### Static Mode (default):
Each row represents an ROI, and columns contain the requested measures.

| roi      | mean  | median | std   | count |
|----------|-------|--------|-------|-------|
| roi1     | 3.5   | 3.0    | 1.2   | 10    |
| roi2     | 2.8   | 2.5    | 0.8   | 12    |

#### Dynamic Mode (`--dynamic`):
Each row represents a frame for each ROI. Columns include `frame`, `roi` identifier, and the requested measures.

| frame | roi   | mean  | median | std   |
|-------|-------|-------|--------|-------|
| 0     | roi1  | 1.0   | 1.0    | 0.3   |
| 1     | roi1  | 3.0   | 3.0    | 0.5   |
| 2     | roi1  | 4.0   | 4.0    | 0.4   |
| 0     | roi2  | 2.5   | 2.5    | 0.2   |
| 1     | roi2  | 3.3   | 3.3    | 0.4   |
| 2     | roi2  | 4.2   | 4.0    | 0.3   |

#### Dynamic Mode with Acquisition Information:
If the `--acquisition_information` argument is provided, additional columns such as `frame_start` and `frame_duration` are added to the dataframe. The frame times correspond to the `frame` column.

| frame | roi   | mean  | frame_start | frame_duration | frame_center |
|-------|-------|-------|-------------|----------------|--------------|
| 0     | roi1  | 1.0   | 0           | 10             | 5            |
| 1     | roi1  | 3.0   | 10          | 10             | 15           |
| 2     | roi1  | 4.0   | 20          | 10             | 25           |
| 0     | roi2  | 2.5   | 0           | 10             | 5            |
| 1     | roi2  | 3.3   | 10          | 10             | 15           |
| 2     | roi2  | 4.2   | 20          | 10             | 25           |


In this example, `frame_start`, `frame_duration`, and `frame_duration` are derived from the acquisition sidecar.

### ToDo

- Parallelize the extraction to process ROIs in parallel, which could be beneficial for larger dynamic images.
- Add a checker to automatically distinguish between dynamic and static data based on the image dimensions.
