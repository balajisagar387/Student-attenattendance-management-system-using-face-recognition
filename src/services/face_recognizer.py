"""Real-time face recognition and live attendance pipeline with strict dual-metric SFace model."""
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import cv2
import numpy as np
from config.settings import settings
from src.core.db import db
from src.core.logger import logger
from src.services.face_enrollment import face_enrollment_service

class FaceRecognizerService:
    def __init__(self):
        self.recognizer = None
        self.detector = None
        self.enrolled_cache: List[Dict[str, Any]] = []
        self.last_logged: Dict[str, float] = {} # student_id -> last_timestamp
        self.cooldown_seconds: float = 30.0

        # Strict Thresholds:
        # Same person with landmark alignment: Cosine >= 0.80, L2 <= 0.40
        # Different person: Cosine < 0.35, L2 > 1.15
        self.MATCH_THRESHOLD: float = settings.FACE_MATCH_THRESHOLD # Default 0.52
        self.MAX_L2_DISTANCE: float = settings.FACE_MAX_L2_DISTANCE # Default 0.98

        self.init_models()
        self.reload_enrolled_cache()

    def init_models(self):
        """Load OpenCV YuNet detector and SFace recognizer."""
        try:
            yunet_model = settings.BASE_DIR / "data" / "face_detection_yunet.onnx"
            sface_model = settings.BASE_DIR / "data" / "face_recognition_sface.onnx"

            if yunet_model.exists():
                self.detector = cv2.FaceDetectorYN.create(str(yunet_model), "", (320, 320), 0.5)
                logger.info("OpenCV YuNet face detector loaded.")

            if sface_model.exists():
                self.recognizer = cv2.FaceRecognizerSF.create(str(sface_model), "")
                logger.info("OpenCV SFace deep neural network loaded for face recognition.")
        except Exception as e:
            logger.error(f"Error initializing face models: {e}")

    def reload_enrolled_cache(self):
        """Pre-cache enrolled student vectors and re-encode with landmark alignment."""
        try:
            records = db.fetch_all("SELECT student_id, name, roll_no, department, photo_path, face_embedding FROM students")
            cache = []
            for r in records:
                embedding = None
                raw_blob = r.get("face_embedding")
                if raw_blob:
                    try:
                        embedding = np.frombuffer(raw_blob, dtype=np.float32)
                    except Exception:
                        embedding = None

                # Recompute and update DB if photo is available to guarantee aligned embedding
                if r.get("photo_path"):
                    photo_file = settings.BASE_DIR / r["photo_path"]
                    if photo_file.exists():
                        img = cv2.imread(str(photo_file))
                        if img is not None:
                            aligned_vec = face_enrollment_service.extract_embedding(img)
                            if aligned_vec is not None and len(aligned_vec) == face_enrollment_service.EMBEDDING_DIM:
                                embedding = aligned_vec
                                try:
                                    db.execute("UPDATE students SET face_embedding = %s WHERE student_id = %s", 
                                               (embedding.tobytes(), r["student_id"]))
                                except Exception:
                                    pass

                if embedding is not None and len(embedding) == face_enrollment_service.EMBEDDING_DIM:
                    cache.append({
                        "student_id": str(r["student_id"]),
                        "name": r["name"],
                        "roll_no": r["roll_no"],
                        "department": r["department"],
                        "embedding": embedding
                    })

            self.enrolled_cache = cache
            logger.info(f"Enrolled student cache reloaded: {len(self.enrolled_cache)} students loaded in memory.")
        except Exception as e:
            logger.error(f"Error loading student face cache: {e}")

    def recognize_faces_in_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect all faces in the camera frame using YuNet, align each face using its
        5 facial landmarks, and match against enrolled students with strict dual metrics:
        1. Cosine similarity >= MATCH_THRESHOLD (0.52)
        2. L2 Euclidean distance <= MAX_L2_DISTANCE (0.98)

        Returns list of detection dicts:
            [{
                "box": (x, y, w, h),
                "is_match": bool,
                "candidate": Optional[Dict],
                "confidence": float,
                "cosine": float,
                "l2": float
            }, ...]
        """
        results = []
        if frame is None or frame.size == 0 or not self.detector or not self.recognizer:
            return results

        h, w = frame.shape[:2]
        self.detector.setInputSize((w, h))
        _, faces = self.detector.detect(frame)

        if faces is None or len(faces) == 0:
            return results

        for f in faces:
            box = (int(f[0]), int(f[1]), int(f[2]), int(f[3]))

            # 1. Canonical 5-landmark alignment
            try:
                aligned = self.recognizer.alignCrop(frame, f)
                feat = self.recognizer.feature(aligned).flatten().astype(np.float32)
                norm = np.linalg.norm(feat)
                if norm > 0:
                    feat /= norm
            except Exception as e:
                logger.error(f"Error aligning face in frame: {e}")
                continue

            best_match = None
            best_cosine = -1.0
            best_l2 = 999.0

            for candidate in self.enrolled_cache:
                cand_vec = candidate["embedding"]
                cos_score = float(self.recognizer.match(feat, cand_vec, cv2.FaceRecognizerSF_FR_COSINE))
                l2_dist = float(self.recognizer.match(feat, cand_vec, cv2.FaceRecognizerSF_FR_NORM_L2))

                if cos_score > best_cosine:
                    best_cosine = cos_score
                    best_l2 = l2_dist
                    best_match = candidate

            # STRICT DUAL CRITERIA:
            # Must satisfy BOTH high cosine similarity AND low Euclidean distance
            is_match = (
                best_match is not None and 
                best_cosine >= self.MATCH_THRESHOLD and 
                best_l2 <= self.MAX_L2_DISTANCE
            )

            if is_match:
                # Scaled display percentage (0.50 -> 72%, 0.90+ -> 99%)
                display_conf = min(0.99, max(0.70, (best_cosine - 0.40) / 0.55))
            else:
                display_conf = max(0.0, best_cosine)

            results.append({
                "box": box,
                "is_match": is_match,
                "candidate": best_match if is_match else None,
                "confidence": display_conf,
                "cosine": best_cosine,
                "l2": best_l2
            })

        return results

    def recognize_face(self, face_crop: np.ndarray) -> Tuple[bool, Optional[Dict[str, Any]], float]:
        """
        Fallback single-crop recognizer with strict dual-metric verification.
        """
        if not self.enrolled_cache or face_crop is None or face_crop.size == 0:
            return False, None, 0.0

        query_vec = face_enrollment_service.extract_embedding(face_crop)
        if query_vec is None or query_vec.size == 0 or np.all(query_vec == 0):
            return False, None, 0.0

        best_match = None
        best_cosine = -1.0
        best_l2 = 999.0

        for candidate in self.enrolled_cache:
            cand_vec = candidate["embedding"]
            if self.recognizer:
                cos = float(self.recognizer.match(query_vec.reshape(1, -1), cand_vec.reshape(1, -1), cv2.FaceRecognizerSF_FR_COSINE))
                l2 = float(self.recognizer.match(query_vec.reshape(1, -1), cand_vec.reshape(1, -1), cv2.FaceRecognizerSF_FR_NORM_L2))
            else:
                cos = float(np.dot(query_vec, cand_vec))
                l2 = float(np.linalg.norm(query_vec - cand_vec))

            if cos > best_cosine:
                best_cosine = cos
                best_l2 = l2
                best_match = candidate

        is_match = (
            best_match is not None and 
            best_cosine >= self.MATCH_THRESHOLD and 
            best_l2 <= self.MAX_L2_DISTANCE
        )

        if is_match:
            display_conf = min(0.99, max(0.70, (best_cosine - 0.40) / 0.55))
            return True, best_match, display_conf

        return False, None, max(0.0, best_cosine)

    def should_record_attendance(self, student_id: str) -> bool:
        """Check debounce cooldown to avoid logging same student repeatedly."""
        now = time.time()
        last_time = self.last_logged.get(student_id, 0.0)
        if now - last_time > self.cooldown_seconds:
            self.last_logged[student_id] = now
            return True
        return False

face_recognizer_service = FaceRecognizerService()
