"""Real-time face recognition and live attendance pipeline with SFace Deep Model."""
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
        self.enrolled_cache: List[Dict[str, Any]] = []
        self.last_logged: Dict[str, float] = {} # student_id -> last_timestamp
        self.cooldown_seconds: float = 30.0    # Minimum seconds between repeated live matches
        self.MATCH_THRESHOLD: float = 0.38     # SFace cosine similarity threshold (different people score < 0.20)
        self.init_sface()
        self.reload_enrolled_cache()

    def init_sface(self):
        """Load OpenCV SFace model for cosine distance matching."""
        try:
            sface_model = settings.BASE_DIR / "data" / "face_recognition_sface.onnx"
            if sface_model.exists():
                self.recognizer = cv2.FaceRecognizerSF.create(str(sface_model), "")
                logger.info("OpenCV SFace deep neural network loaded for face recognition.")
        except Exception as e:
            logger.error(f"Error initializing SFace recognizer: {e}")

    def reload_enrolled_cache(self):
        """Pre-cache enrolled student vectors and metadata in memory for fast matching."""
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
                
                # If no embedding stored or length mismatch, recompute from photo
                if (embedding is None or len(embedding) != face_enrollment_service.EMBEDDING_DIM) and r.get("photo_path"):
                    photo_file = settings.BASE_DIR / r["photo_path"]
                    if photo_file.exists():
                        img = cv2.imread(str(photo_file))
                        if img is not None:
                            embedding = face_enrollment_service.extract_embedding(img)
                            # Update DB with clean vector
                            try:
                                db.execute("UPDATE students SET face_embedding = %s WHERE student_id = %s", 
                                           (embedding.tobytes(), r["student_id"]))
                            except Exception:
                                pass

                if embedding is not None and len(embedding) == face_enrollment_service.EMBEDDING_DIM:
                    cache.append({
                        "student_id": r["student_id"],
                        "name": r["name"],
                        "roll_no": r["roll_no"],
                        "department": r["department"],
                        "embedding": embedding
                    })

            self.enrolled_cache = cache
            logger.info(f"Enrolled student cache reloaded: {len(self.enrolled_cache)} students loaded in memory.")
        except Exception as e:
            logger.error(f"Error loading student face cache: {e}")

    def recognize_face(self, face_crop: np.ndarray) -> Tuple[bool, Optional[Dict[str, Any]], float]:
        """
        Compare face crop against memory cache using SFace deep feature cosine similarity.
        Returns:
            (is_match, student_data, confidence_score)
        """
        if not self.enrolled_cache or face_crop is None or face_crop.size == 0:
            return False, None, 0.0

        query_vec = face_enrollment_service.extract_embedding(face_crop)
        if query_vec is None or query_vec.size == 0 or np.all(query_vec == 0):
            return False, None, 0.0

        best_match = None
        best_score = -1.0

        for candidate in self.enrolled_cache:
            cand_vec = candidate["embedding"]
            
            if self.recognizer:
                try:
                    score = float(self.recognizer.match(
                        query_vec.reshape(1, -1),
                        cand_vec.reshape(1, -1),
                        cv2.FaceRecognizerSF_FR_COSINE
                    ))
                except Exception:
                    score = float(np.dot(query_vec, cand_vec))
            else:
                score = float(np.dot(query_vec, cand_vec))

            if score > best_score:
                best_score = score
                best_match = candidate

        # Strict threshold: Must exceed MATCH_THRESHOLD (0.38)
        is_match = (best_score >= self.MATCH_THRESHOLD)
        
        # Format intuitive display percentage
        if is_match:
            display_conf = min(0.99, max(0.65, (best_score - 0.20) / 0.70))
            return True, best_match, display_conf
        
        return False, None, max(0.0, best_score)

    def should_record_attendance(self, student_id: str) -> bool:
        """Check debounce cooldown to avoid logging same student repeatedly."""
        now = time.time()
        last_time = self.last_logged.get(student_id, 0.0)
        if now - last_time > self.cooldown_seconds:
            self.last_logged[student_id] = now
            return True
        return False

face_recognizer_service = FaceRecognizerService()
