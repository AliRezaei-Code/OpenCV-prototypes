import cv2
import time
from typing import Iterator, Union, Tuple, Optional

class VideoSource:
    def __init__(self, source: Union[int, str] = 0, width: int = 1280, height: int = 720):
        """
        Initialize Video Capture.
        source: 0 for webcam, or path to video file.
        """
        self.source = source
        self.cap = cv2.VideoCapture(source)
        
        if isinstance(source, int):
            # Set resolution for webcams
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video source: {source}")

    def __iter__(self) -> Iterator[Tuple[float, np.ndarray]]:
        """
        Yields (timestamp, frame).
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            timestamp = time.time()
            yield timestamp, frame
            
    def release(self):
        self.cap.release()

    def get_fps(self) -> float:
        return self.cap.get(cv2.CAP_PROP_FPS)

import numpy as np
