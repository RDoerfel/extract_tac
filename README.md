# extract_tac
This is a simple tool to extract tacs and mean values from a (dynamic) image given a segmetnation mask.

## Installation
Easily install it from github with pip:
```bash
pip install git+https://github.com/RDoerfel/extract_tac.git
```

## Command Line Interface

The tool provides a command-line interface for extracting Time Activity Curves (TACs) or single values from images based on specified masks and regions of interest (ROIs).

### Usage

```bash
python -m extract_tac --image <image_path> --mask <mask_path> --rois <rois_path> --output <output_path> [options]
```

### Required Arguments

- `--image`: Path to the input image file
  - Example: `--image /path/to/pet_image.nii.gz`

- `--mask`: Path to the mask file
  - Example: `--mask /path/to/brain_mask.nii.gz`

- `--rois`: Path to the ROIs file containing region definitions
  - Example: `--rois /path/to/regions.json`

- `--output`: Path where the output will be saved
  - Example: `--output /path/to/results.csv`

### ROI Definition File Format

The ROI definition file should be in JSON format, where each ROI is defined with a name and corresponding index values. The index should corespond to values in your mask image. Here's the expected structure:

```json
[
    {
        "name": "insula",
        "index": [
            1035,
            2035
        ]
    },
    {
        "name": "temporal-lobe",
        "index": [
            1001,
            1009,
            1015,
            1030,
            1034,
            2001,
            2009,
            2015,
            2030,
            2034
        ]
    },
]
```
I provided some examples [examples](./bin) for the Freesurfer aseg+aparc segmentations. 

In general, each ROI entry contains:
- `name`: A string identifier for the region
- `index`: An array of integer values representing the indices that define this region in the mask. For custom masks, this will typically be a single value.

### Optional Arguments

- `--measure`: Specify one or more statistical measures to extract
  - Available options: `mean`, `median`, `std`, `count`
  - Default: All measures (`mean`, `median`, `std`, `count`)
  - Example for single measure: `--measure mean`
  - Example for multiple measures: `--measure mean std`

- `--dynamic`: Flag to extract time activity curves
  - If present: Extracts TACs over time
  - If absent: Extracts single values per ROI
  - Example: `--dynamic`

### Examples

1. Extract mean and standard deviation from a static image:
```bash
python -m extract_tac --image pet.nii.gz --mask brain.nii.gz --rois regions.json --output results.csv --measure mean std
```

2. Extract all measures and generate TACs:
```bash
python -m extract_tac --image dynamic_pet.nii.gz --mask brain.nii.gz --rois regions.json --output tacs.csv --dynamic
```

3. Extract only median values from a static image:
```bash
python -m extract_tac --image pet.nii.gz --mask brain.nii.gz --rois regions.json --output median_values.csv --measure median
```

### Output Format

The tool generates a CSV file containing the requested measurements. The format varies depending on whether dynamic mode is enabled:

- Static mode (default):
  - Each row represents an ROI
  - Columns contain the requested measures

- Dynamic mode (`--dynamic`):
  - Each row represents a timepoint for each ROI
  - Columns include timepoint, ROI identifier, and requested measures


### ToDo
- parallelize the extraction to run rois in parallel. Might be useful for larger dynamic images.
- add proper documentation
- add tests for higher-order functions
- add progress bar / information to console output
- add a checker for dynamic or static. Should be easy via dimensions
- distribute the standard fs regions with the package
