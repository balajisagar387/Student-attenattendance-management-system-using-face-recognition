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
        self.detector = None
        self.init_models()

    def init_models(self):
        """Initialize OpenCV SFace Deep Face Recognition Model and YuNet detector."""
        try:
            yunet_model = settings.BASE_DIR / "data" / "face_detection_yunet.onnx"
            sface_model = settings.BASE_DIR / "data" / "face_recognition_sface.onnx"
            if yunet_model.exists():
                self.detector = cv2.FaceDetectorYN.create(str(yunet_model), "", (320, 320), 0.5)
            if sface_model.exists():
                self.recognizer = cv2.FaceRecognizerSF.create(str(sface_model), "")
                logger.info("OpenCV SFace deep neural network initialized for face enrollment.")
            else:
                logger.warning(f"SFace model file not found at {sface_model}")
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")

    def extract_embedding(self, img: np.ndarray) -> np.ndarray:
        """
        Extract 128-dimensional deep feature embedding from face image using landmark alignment (alignCrop).
        """
        if img is None or img.size == 0:
            return np.zeros(self.EMBEDDING_DIM, dtype=np.float32)

        if not self.recognizer or not self.detector:
            self.init_models()

        try:
            h, w = img.shape[:2]
            if self.detector:
                self.detector.setInputSize((w, h))
                _, faces = self.detector.detect(img)
                if faces is not None and len(faces) > 0 and self.recognizer:
                    aligned = self.recognizer.alignCrop(img, faces[0])
                    feat = self.recognizer.feature(aligned)
                    vec = feat.flatten().astype(np.float32)
                    norm = np.linalg.norm(vec)
                    if norm > 0:
                        vec = vec / norm
                    return vec

            # Fallback to direct resize if YuNet did not catch tight crop
            if self.recognizer:
                resized = cv2.resize(img, (112, 112))
                feat = self.recognizer.feature(resized)
                vec = feat.flatten().astype(np.float32)
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
                return vec
        except Exception as e:
            logger.error(f"SFace feature extraction failed: {e}")

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
