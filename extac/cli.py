import argparse
from pathlib import Path
from extac.wrapper import extract_tacs


def main():
    parser = argparse.ArgumentParser(description="Extract TACs or single values from images")
    parser.add_argument("--image", type=Path, required=True, help="Path to the cerebellum segmentation file")
    parser.add_argument("--mask", type=Path, required=True, help="Path to the brain segmentation file")
    parser.add_argument("--rois", type=Path, required=True, help="Path to the output reference region file")
    parser.add_argument("--output", type=Path, required=True, help="Path to the output file")
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
    args = parser.parse_args()
    extract_tacs(args.image, args.mask, args.rois, args.output, args.measure, args.dynamic)


if __name__ == "__main__":
    main()
