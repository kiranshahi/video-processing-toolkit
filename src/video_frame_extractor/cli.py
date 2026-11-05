import argparse
from .extractor import save_frames


def main(): 
    
    parser = argparse.ArgumentParser( description="Extract frames from videos")
    parser.add_argument("video", help="Input video path")
    parser.add_argument("-o", "--output", default="frames")
    parser.add_argument("--fps", type=float, default=None)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--end", type=float, default=None)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)

    args = parser.parse_args()

    if (args.width is None) != (args.height is None):
        parser.error("--width and --height must be used together")

    resize = ((args.width, args.height) if args.width is not None else None)

    count = save_frames(args.video, args.output, fps=args.fps, start=args.start, end=args.end, resize=resize,)

    print(f"Saved {count} frames to {args.output}")
