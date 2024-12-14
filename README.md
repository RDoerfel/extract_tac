# extract_tac
This is a simple tool to extract tacs and mean values from a (dynamic) image given a segmetnation mask.

## Installation
Easily install it from github with pip:
```bash
pip install git+https://github.com/RDoerfel/extract_tac.git
```

## Usage
```bash
extract_tac --image image_file --mask mask_file --rois roi_file --output output_file --dynamic
```
There are generally two modes to extract tacs: static and dynamic. This is indicated by the flag `--dynamic`. In static mode, the image is a static image (only one frame). In dynamic mode, the image is a dynamic image such as acquired during PET imaging. 

Carefule, at the moment there is no check whether the image is actually dynamic or not. so the user should be aware of the image type ;).

The rois file is a json file with the following format:
```
{
    "roi1": [1, 2, 3],
    "roi2": [4, 5, 6],
}
```
There are some example images and rois in the `bin` folder. The examples are based on the aparc+aseg segmentation provided by FreeSurfer. But generally, any mask and appropriate rois file should work. There need to be a corresponding index in the mask for each roi. 

The output file is a csv file with the following format is a .tsv file that contains the mean for each roi in the .json file. It currently looks like this:
```tsv
roi1	roi2
0.1 0.2
0.3 0.4
0.5 0.6
```

### ToDo
- parallelize the extraction to run rois in parallel. Might be useful for larger dynamic images.
- add proper documentation
- add tests for higher-order functions
- add progress bar / information to console output
- add a checker for dynamic or static. Should be easy via dimensions
- distribute the standard fs regions with the package
