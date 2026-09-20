"""Pose estimation and face quality analysis using Google MediaPipe."""
import math
from typing import Dict, Any, Optional, Tuple
import cv2
import numpy as np
from config.settings import settings
from config.constants import (
    MSG_LOOK_STRAIGHT,
    MSG_HEAD_LEVEL,
    MSG_HEAD_STRAIGHT,
    MSG_MOVE_CLOSER,
    MSG_STEP_BACK,
    MSG_CENTER_FACE,
    MSG_TOO_BLURRY,
    MSG_PERFECT,
)
from src.core.logger import logger

class PoseEstimator:
    def __init__(self):
        self.mp_face_mesh = None
        self.face_mesh = None
        self.init_mediapipe()

    def init_mediapipe(self):
        """Initialize MediaPipe Face Mesh."""
        try:
            import mediapipe as mp
            self.mp_face_mesh = mp.solutions.face_mesh
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            logger.info("MediaPipe Face Mesh initialized successfully.")
        except Exception as e:
            logger.warning(f"MediaPipe not available ({e}). Fallback mode active.")
            self.face_mesh = None

    def evaluate_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate frame for face alignment, head pose, framing, and clarity.
        Returns:
            {
                "face_detected": bool,
                "is_valid": bool,
                "message": str,
                "color_bgr": Tuple[int, int, int],
                "box": Optional[Tuple[int, int, int, int]], # x, y, w, h
                "crop": Optional[np.ndarray],
                "metrics": dict
            }
        """
        h, w, _ = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 1. Blurriness Check
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < settings.MIN_LAPLACIAN_VAR:
            return {
                "face_detected": False,
                "is_valid": False,
                "message": MSG_TOO_BLURRY,
                "color_bgr": (0, 165, 255), # Orange
                "box": None,
                "crop": None,
                "metrics": {"blur": laplacian_var}
            }

        # 2. Face Detection & Landmark Extraction via MediaPipe
        if self.face_mesh:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)

            if not results.multi_face_landmarks:
                return {
                    "face_detected": False,
                    "is_valid": False,
                    "message": "No face detected in camera view",
                    "color_bgr": (0, 0, 255), # Red
                    "box": None,
                    "crop": None,
                    "metrics": {}
                }

            landmarks = results.multi_face_landmarks[0].landmark

            # Extract 2D pixel coordinates
            pts = np.array([(int(p.x * w), int(p.y * h)) for p in landmarks])
            min_x, min_y = np.min(pts, axis=0)
            max_x, max_y = np.max(pts, axis=0)

            # Add margin
            margin_x = int((max_x - min_x) * 0.15)
            margin_y = int((max_y - min_y) * 0.20)
            x1 = max(0, min_x - margin_x)
            y1 = max(0, min_y - margin_y)
            x2 = min(w, max_x + margin_x)
            y2 = min(h, max_y + margin_y)
            box = (x1, y1, x2 - x1, y2 - y1)

            # Extract Landmark Reference Points
            # 1: Nose tip, 152: Chin, 33: Left eye outer, 263: Right eye outer
            nose = pts[1]
            chin = pts[152]
            left_eye = pts[33]
            right_eye = pts[263]

            # Calculate Head Pose Metrics
            # Roll: Angle between eyes
            eye_delta_x = right_eye[0] - left_eye[0]
            eye_delta_y = right_eye[1] - left_eye[1]
            roll_angle = math.degrees(math.atan2(eye_delta_y, eye_delta_x))

            # Yaw: Ratio of distance from nose to left vs right eye
            dist_left = np.linalg.norm(nose - left_eye)
            dist_right = np.linalg.norm(nose - right_eye)
            total_eye_dist = dist_left + dist_right
            yaw_ratio = (dist_right - dist_left) / (total_eye_dist + 1e-6)
            yaw_angle = yaw_ratio * 90.0 # Approximate degrees

            # Pitch: Vertical nose position between eye level and chin
            eye_center_y = (left_eye[1] + right_eye[1]) / 2.0
            dist_nose_eyes = nose[1] - eye_center_y
            dist_nose_chin = chin[1] - nose[1]
            pitch_ratio = (dist_nose_chin - dist_nose_eyes) / (dist_nose_chin + dist_nose_eyes + 1e-6)
            pitch_angle = (pitch_ratio - 0.2) * 60.0 # Adjusted offset

            # Framing & Scale Check
            face_height = y2 - y1
            face_scale = face_height / float(h)
            center_x = (x1 + x2) / 2.0
            frame_center_offset = abs(center_x - (w / 2.0)) / float(w)

            # Evaluate Pose Guidance Conditions
            color_bgr = (0, 255, 0) # Green (Default Valid)
            is_valid = True
            msg = MSG_PERFECT

            if abs(yaw_angle) > settings.MAX_YAW_ANGLE:
                is_valid = False
                color_bgr = (0, 215, 255) # Yellow
                msg = MSG_LOOK_STRAIGHT
            elif abs(pitch_angle) > settings.MAX_PITCH_ANGLE:
                is_valid = False
                color_bgr = (0, 215, 255)
                msg = MSG_HEAD_LEVEL
            elif abs(roll_angle) > settings.MAX_ROLL_ANGLE:
                is_valid = False
                color_bgr = (0, 215, 255)
                msg = MSG_HEAD_STRAIGHT
            elif face_scale < settings.MIN_FACE_SCALE:
                is_valid = False
                color_bgr = (0, 215, 255)
                msg = MSG_MOVE_CLOSER
            elif face_scale > settings.MAX_FACE_SCALE:
                is_valid = False
                color_bgr = (0, 215, 255)
                msg = MSG_STEP_BACK
            elif frame_center_offset > 0.25:
                is_valid = False
                color_bgr = (0, 215, 255)
                msg = MSG_CENTER_FACE

            crop = frame[y1:y2, x1:x2].copy()

            return {
                "face_detected": True,
                "is_valid": is_valid,
                "message": msg,
                "color_bgr": color_bgr,
                "box": box,
                "crop": crop,
                "metrics": {
                    "yaw": round(yaw_angle, 1),
                    "pitch": round(pitch_angle, 1),
                    "roll": round(roll_angle, 1),
                    "scale": round(face_scale, 2),
                    "blur": round(laplacian_var, 0)
                }
            }

        # Fallback using OpenCV Haar Cascade if MediaPipe is not installed
        return self._evaluate_haar_fallback(frame, gray, laplacian_var)

    def _evaluate_haar_fallback(self, frame: np.ndarray, gray: np.ndarray, blur: float) -> Dict[str, Any]:
        """Fallback evaluation using standard OpenCV Haar Cascade."""
        h, w, _ = frame.shape
        local_cascade = settings.BASE_DIR / "face_classifier.xml"
        if local_cascade.exists():
            cascade = cv2.CascadeClassifier(str(local_cascade))
        else:
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            cascade = cv2.CascadeClassifier(cascade_path)

        faces = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        if len(faces) == 0:
            return {
                "face_detected": False,
                "is_valid": False,
                "message": "No face detected in camera view",
                "color_bgr": (0, 0, 255),
                "box": None,
                "crop": None,
                "metrics": {"face_count": 0, "blur": blur}
            }

        # Enforce exactly one face in the frame
        if len(faces) > 1:
            return {
                "face_detected": True,
                "is_valid": False,
                "message": "⚠️ Multiple faces detected! Only ONE person allowed in frame.",
                "color_bgr": (0, 0, 255),
                "box": None,
                "crop": None,
                "metrics": {"face_count": len(faces), "blur": blur}
            }

        # Exactly 1 face detected
        (x, y, fw, fh) = faces[0]
        crop = frame[y:y+fh, x:x+fw].copy()
        face_scale = fh / float(h)
        center_x = (x + fw / 2.0) / float(w)
        center_y = (y + fh / 2.0) / float(h)

        # Symmetry analysis for head pose (looking straight vs turned)
        face_gray = gray[y:y+fh, x:x+fw]
        symmetry_score = 1.0
        if fw > 40 and fh > 40:
            mid_w = fw // 2
            left_half = face_gray[:, :mid_w]
            right_half = face_gray[:, mid_w:mid_w*2]
            if left_half.shape == right_half.shape and left_half.size > 0:
                right_flipped = cv2.flip(right_half, 1)
                l_std = cv2.resize(left_half, (64, 64))
                r_std = cv2.resize(right_flipped, (64, 64))
                res = cv2.matchTemplate(l_std, r_std, cv2.TM_CCOEFF_NORMED)
                symmetry_score = float(res[0][0])

        is_valid = True
        color_bgr = (0, 255, 0) # Green
        msg = MSG_PERFECT

        if face_scale < settings.MIN_FACE_SCALE:
            is_valid = False
            color_bgr = (0, 215, 255) # Yellow
            msg = "👉 Move a little closer to the camera"
        elif face_scale > settings.MAX_FACE_SCALE:
            is_valid = False
            color_bgr = (0, 215, 255)
            msg = "👈 Step back slightly from the camera"
        elif abs(center_x - 0.5) > 0.22 or abs(center_y - 0.45) > 0.22:
            is_valid = False
            color_bgr = (0, 215, 255)
            msg = "🎯 Center your face inside the oval guide"
        elif symmetry_score < 0.30:
            is_valid = False
            color_bgr = (0, 215, 255)
            msg = "👀 Look straight at the camera"
        elif blur < settings.MIN_LAPLACIAN_VAR:
            is_valid = False
            color_bgr = (0, 215, 255)
            msg = "💡 Hold still (camera adjusting / low lighting)"

        return {
            "face_detected": True,
            "is_valid": is_valid,
            "message": msg,
            "color_bgr": color_bgr,
            "box": (x, y, fw, fh),
            "crop": crop,
            "metrics": {
                "scale": round(face_scale, 2),
                "symmetry": round(symmetry_score, 2),
                "blur": round(blur, 0),
                "face_count": 1
            }
        }

pose_estimator = PoseEstimator()
