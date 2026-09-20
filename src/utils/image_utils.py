"""Image processing, conversion, and caching utilities."""
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageTk
import cv2
import numpy as np
from src.core.logger import logger

class ImageUtils:
    @staticmethod
    def get_resampling_filter():
        """Ensure compatibility with Pillow 10+ where ANTIALIAS was removed."""
        if hasattr(Image, "Resampling"):
            return Image.Resampling.LANCZOS
        return getattr(Image, "ANTIALIAS", Image.BICUBIC)

    @classmethod
    def load_and_resize(cls, image_path: Path, size: Tuple[int, int]) -> Optional[ImageTk.PhotoImage]:
        """Safely load and resize an image from disk using modern LANCZOS filter."""
        try:
            if not image_path.exists():
                logger.warning(f"Image not found: {image_path}")
                return None
            img = Image.open(str(image_path))
            resample = cls.get_resampling_filter()
            img = img.resize(size, resample)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None

    @classmethod
    def cv2_to_photoimage(cls, frame: np.ndarray, size: Optional[Tuple[int, int]] = None) -> ImageTk.PhotoImage:
        """Convert an OpenCV BGR numpy frame into a Tkinter PhotoImage."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)
        if size:
            resample = cls.get_resampling_filter()
            pil_img = pil_img.resize(size, resample)
        return ImageTk.PhotoImage(image=pil_img)

image_utils = ImageUtils()
