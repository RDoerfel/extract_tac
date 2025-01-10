import argparse
from pathlib import Path
from extac.extract_tacs import extract_tacs


def main():
    parser = argparse.ArgumentParser(description="Extract TACs or single values from images")
    parser.add_argument("--image", type=Path, required=True, help="Path to the cerebellum segmentation file")
    parser.add_argument("--mask", type=Path, required=True, help="Path to the brain segmentation file")
    parser.add_argument("--rois", type=Path, required=True, help="Path to the output reference region file")
    parser.add_argument("--output", type=Path, required=True, help="Path to the output file")
    parser.add_argument(
        "--acquisition_information",
        type=Path,
        help=" Path to json sidecar that contains the frame timing information. Should follow BIDS notation. \
        Additional information such as FrameTimeStart, FrameDuration will be added.",
        default=None,
    )
    parser.add_argument(
        "--measure",
        type=str,
        nargs="+",
        default=["mean", "median", "std", "count"],
        choices=["mean", "median", "std", "count"],
        help="One or more measures to extract",
    )
    parser.add_argument(
        "--dynamic",
        action="store_true",
        help="If True, extract TACs. If False, extract only the measure per ROI values",
    )
    parser.add_argument(
        "--max_workers",
        type=int,
        default=1,
        help="Maximum number of workers for parallel processing. Defaults to 1.",
    )
    args = parser.parse_args()
    extract_tacs(
        image_file=args.image,
        mask_file=args.mask,
        roi_file=args.rois,
        output_file=args.output,
        measures=args.measure,
        dynamic=args.dynamic,
        acquision_information_file=args.acquisition_information,
        max_workers=args.max_workers,
    )


if __name__ == "__main__":
    main()
