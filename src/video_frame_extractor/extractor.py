
from pathlib import Path
from collections.abc import Iterator

import cv2
import numpy as np

# Fetch (timestamp_seconds, frame) from a video.

def extract_frames(video_path: str, fps: float | None = None, start: float = 0.0, end: float | None = None, resize: tuple[int, int] | None = None) -> Iterator[tuple[float, np.ndarray]]:
    
    if fps is not None and fps <= 0:
        raise ValueError("fps must be positive")
    
    if start < 0 or (end is not None and end <= start):
        raise ValueError("Invalid time range")
    
    if resize is not None and any(x <= 0 for x in resize):
        raise ValueError("Resize dimensions must be positive")

    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    try:
        source_fps = cap.get(cv2.CAP_PROP_FPS)
        if source_fps <= 0:
            raise ValueError("Could not determine source FPS")
        if fps is not None and fps > source_fps:
            raise ValueError("Requested FPS exceeds source FPS")

        interval = 1.0 / fps if fps is not None else None
        next_sample = start
        frame_index = 0

        while True:
            success, frame = cap.read()
            if not success:
                break

            timestamp = frame_index / source_fps
            frame_index += 1

            if timestamp < start:
                continue
            if end is not None and timestamp >= end:
                break

            if interval is not None:
                if timestamp + 1e-9 < next_sample:
                    continue
                next_sample += interval

            if resize is not None:
                frame = cv2.resize(frame, resize)

            yield timestamp, frame
    finally:
        cap.release()


# Extract and save frames as JPEG images.
def save_frames(video_path: str, output_dir: str, fps: float | None = None, start: float = 0.0, end: float | None = None, resize: tuple[int, int] | None = None) -> int:

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    count = 0
    for count, (_, frame) in enumerate(
        extract_frames(video_path, fps, start, end, resize),
        start=1,
    ):
        filename = output / f"frame_{count:06d}.jpg"
        if not cv2.imwrite(str(filename), frame):
            raise OSError(f"Could not write {filename}")

    return count
