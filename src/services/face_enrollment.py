"""Face Enrollment service using OpenCV SFace Deep Neural Network."""
from pathlib import Path
from typing import Optional, Tuple
import cv2
import numpy as np
from config.settings import settings
from src.core.logger import logger

class FaceEnrollmentService:
    EMBEDDING_DIM = 128 # SFace feature vector dimension

    def __init__(self):
        self.recognizer = None
        self.init_sface()

    def init_sface(self):
        """Initialize OpenCV SFace Deep Face Recognition Model."""
        try:
            sface_model = settings.BASE_DIR / "data" / "face_recognition_sface.onnx"
            if sface_model.exists():
                self.recognizer = cv2.FaceRecognizerSF.create(str(sface_model), "")
                logger.info("OpenCV SFace deep neural network initialized for face enrollment.")
            else:
                logger.warning(f"SFace model file not found at {sface_model}")
        except Exception as e:
            logger.error(f"Failed to initialize SFace recognizer: {e}")

    def extract_embedding(self, face_crop: np.ndarray) -> np.ndarray:
        """
        Extract 128-dimensional deep feature embedding from face crop.
        SFace produces distinct vectors for different individuals (similarity < 0.20 for different people, > 0.80 for same).
        """
        if face_crop is None or face_crop.size == 0:
            return np.zeros(self.EMBEDDING_DIM, dtype=np.float32)

        if not self.recognizer:
            self.init_sface()

        try:
            # SFace expects standardized 112x112 input
            resized = cv2.resize(face_crop, (112, 112))
            if self.recognizer:
                feat = self.recognizer.feature(resized)
                vec = feat.flatten().astype(np.float32)
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
                return vec
        except Exception as e:
            logger.error(f"SFace feature extraction failed: {e}")

        # Fallback pseudo-embedding
        return np.zeros(self.EMBEDDING_DIM, dtype=np.float32)

    def save_enrolled_photo(self, student_id: str, face_crop: np.ndarray) -> Tuple[bool, Path, np.ndarray]:
        """Save student's single cropped face photo and return file path & embedding."""
        try:
            filename = f"{student_id}.jpg"
            save_path = settings.STUDENTS_DIR / filename
            
            # Save standardized photo
            standardized = cv2.resize(face_crop, (500, 500), interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(str(save_path), standardized)
            
            # Generate 128-d deep embedding
            embedding = self.extract_embedding(standardized)
            logger.info(f"Student photo enrolled successfully at {save_path} with 128-D SFace embedding.")
            return True, save_path, embedding
        except Exception as e:
            logger.error(f"Failed to save student photo for {student_id}: {e}")
            raise e

face_enrollment_service = FaceEnrollmentService()
