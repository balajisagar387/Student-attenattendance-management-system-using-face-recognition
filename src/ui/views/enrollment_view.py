"""Interactive Single-Photo Guided Enrollment View with Auto-Capture & Manual Override."""
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional
import cv2
import numpy as np
from PIL import Image, ImageTk
from config.settings import settings
from config.constants import *
from src.core.db import db
from src.core.logger import logger
from src.services.pose_estimator import pose_estimator
from src.services.face_enrollment import face_enrollment_service
from src.utils.image_utils import image_utils
from src.ui.styles import *

class EnrollmentView(tk.Toplevel):
    def __init__(self, master, student_id: str, student_name: str, on_enrolled_callback: Callable):
        super().__init__(master)
        self.student_id = student_id
        self.student_name = student_name
        self.on_enrolled_callback = on_enrolled_callback

        self.title(f"Photo Enrollment - {self.student_name} ({self.student_id})")
        self.geometry("940x740")
        self.minsize(880, 680)
        self.configure(bg=BG_DARK)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.cap = None
        self.is_running = False
        self.is_captured = False
        self.captured_crop = None
        self.latest_detected_crop = None
        self.latest_full_frame = None
        self.captured_photo_img = None
        
        # Stability accumulator for smooth automatic snapshot
        self.stable_frames = 0
        self.REQUIRED_STABLE_FRAMES = 12 # ~0.5 - 0.7 seconds of steady alignment

        self.build_ui()
        self.start_camera()

    def build_ui(self):
        # 1. Header Banner
        header = tk.Frame(self, bg=BG_CARD, height=60, padx=20)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title = tk.Label(header, text=f"Guided Photo Enrollment: {self.student_name}", font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
        title.pack(side=tk.LEFT, pady=15)

        sub = tk.Label(header, text=f"ID: {self.student_id}  |  1 Frontal Photo", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD)
        sub.pack(side=tk.RIGHT, pady=18)

        # 2. Dynamic Status Guidance Banner
        self.guide_banner = tk.Label(
            self, text="Initializing wide-angle camera & guidance...", font=FONT_BODY_BOLD,
            bg=THEME_WARNING, fg=TEXT_PRIMARY, height=2
        )
        self.guide_banner.pack(fill=tk.X, padx=20, pady=(12, 5))

        # 3. Camera Feed Display
        self.cam_frame = tk.Frame(self, bg=BG_CARD, bd=2, relief=tk.SOLID)
        self.cam_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        self.cam_lbl = tk.Label(self.cam_frame, bg="#000000")
        self.cam_lbl.pack(fill=tk.BOTH, expand=True)

        # 4. Action Controls Bar
        controls = tk.Frame(self, bg=BG_CARD, height=75, padx=20)
        controls.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 10))
        controls.pack_propagate(False)

        self.info_lbl = tk.Label(controls, text="Metrics: Detecting...", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD)
        self.info_lbl.pack(side=tk.LEFT, pady=25)

        # Confirm & Save button (active green once captured, grey while aligning)
        self.confirm_btn = tk.Button(
            controls, text="Align Face to Auto-Capture", font=FONT_BODY_BOLD,
            bg="#555555", fg=TEXT_PRIMARY, state=tk.DISABLED, bd=0, cursor="hand2",
            padx=20, pady=8, command=self.save_and_finish
        )
        self.confirm_btn.pack(side=tk.RIGHT, pady=15)

        # Retake button (hidden until captured)
        self.retake_btn = tk.Button(
            controls, text="↺ Retake Photo", font=FONT_BODY_BOLD,
            bg=THEME_WARNING, fg=TEXT_PRIMARY, bd=0, cursor="hand2",
            padx=15, pady=8, command=self.reset_to_live
        )

        # Manual Snap Photo button (allows manual capture at any moment if face is in view)
        self.manual_snap_btn = tk.Button(
            controls, text="📸 Snap Photo Now", font=FONT_BODY_BOLD,
            bg=THEME_PRIMARY, fg=TEXT_PRIMARY, bd=0, cursor="hand2",
            padx=15, pady=8, command=self.manual_snapshot
        )
        self.manual_snap_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=15)

        cancel_btn = tk.Button(
            controls, text="Cancel", font=FONT_BODY, bg=THEME_DANGER, fg=TEXT_PRIMARY,
            bd=0, cursor="hand2", padx=15, pady=8, command=self.on_close
        )
        cancel_btn.pack(side=tk.RIGHT, padx=10, pady=15)

    def start_camera(self):
        """Open camera stream with wide-angle resolution (zoomed out)."""
        try:
            self.cap = cv2.VideoCapture(settings.CAMERA_INDEX)
            # Set wide 16:9 1280x720 mode for wider field of view (less zoomed-in)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            if not self.cap.isOpened():
                self.guide_banner.config(text="ERROR: Could not open camera. Check USB connection.", bg=THEME_DANGER)
                return
            self.is_running = True
            self.process_video_loop()
        except Exception as e:
            logger.error(f"Failed to start camera: {e}")
            self.guide_banner.config(text=f"Camera Error: {e}", bg=THEME_DANGER)

    def process_video_loop(self):
        """Continuous camera frame processing with auto-capture logic."""
        if not self.is_running or not self.cap:
            return

        if self.is_captured:
            return

        ret, frame = self.cap.read()
        if ret and frame is not None:
            frame = cv2.flip(frame, 1)
            self.latest_full_frame = frame.copy()

            # Evaluate face alignment, pose, single-face rule, and clarity
            eval_res = pose_estimator.evaluate_frame(frame)
            is_valid = eval_res["is_valid"]
            message = eval_res["message"]
            color_bgr = eval_res["color_bgr"]
            box = eval_res["box"]
            crop = eval_res["crop"]
            metrics = eval_res.get("metrics", {})

            if crop is not None and crop.size > 0:
                self.latest_detected_crop = crop.copy()
                self.manual_snap_btn.config(state=tk.NORMAL, bg=THEME_PRIMARY)
            else:
                self.manual_snap_btn.config(state=tk.DISABLED, bg="#555555")

            # Draw visual guidance overlay
            h, w, _ = frame.shape
            center_x, center_y = w // 2, int(h * 0.45)
            # Generous spacious oval (zoomed-out comfort)
            oval_axes = (int(w * 0.22), int(h * 0.32))

            # Target Guide Oval
            cv2.ellipse(frame, (center_x, center_y), oval_axes, 0, 0, 360, color_bgr, 3)

            if box:
                bx, by, bw, bh = box
                cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), color_bgr, 2)

            # Prominent On-Screen Guidance Pill at bottom of video
            banner_y = h - 50
            cv2.rectangle(frame, (40, banner_y - 30), (w - 40, banner_y + 15), (25, 25, 25), -1)
            cv2.putText(
                frame, message, (60, banner_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_bgr, 2
            )

            # Auto-Capture State Management with soft accumulator
            if is_valid and crop is not None and crop.size > 0:
                self.stable_frames = min(self.REQUIRED_STABLE_FRAMES, self.stable_frames + 1)
                countdown = max(1, (self.REQUIRED_STABLE_FRAMES - self.stable_frames) // 4 + 1)

                if self.stable_frames >= self.REQUIRED_STABLE_FRAMES:
                    # TRIGGER AUTOMATIC SNAPSHOT
                    self.trigger_snapshot(frame, crop, source="Auto")
                    return
                else:
                    self.guide_banner.config(
                        text=f"✓ PERFECT! HOLD STILL... CAPTURING IN {countdown}s",
                        bg=THEME_SUCCESS
                    )
                    self.confirm_btn.config(
                        text=f"Auto-Capturing in {countdown}s...",
                        state=tk.DISABLED,
                        bg=THEME_WARNING
                    )
            else:
                self.stable_frames = max(0, self.stable_frames - 1)
                bg_color = THEME_WARNING if eval_res["face_detected"] else THEME_DANGER
                self.guide_banner.config(text=f"⚠ {message}", bg=bg_color)
                self.confirm_btn.config(
                    text="Align Face to Auto-Capture",
                    state=tk.DISABLED,
                    bg="#555555"
                )

            # Update Metrics text
            if metrics:
                face_cnt = metrics.get("face_count", 0)
                m_text = f"Faces: {face_cnt} | Scale: {metrics.get('scale', 0)} | Blur: {metrics.get('blur', 0)}"
                self.info_lbl.config(text=m_text)

            photo = image_utils.cv2_to_photoimage(frame, (800, 480))
            self.cam_lbl.config(image=photo)
            self.cam_lbl.image = photo

        self.after(25, self.process_video_loop)

    def manual_snapshot(self):
        """Allow instant manual snapshot whenever a face is detected."""
        if self.latest_detected_crop is None or self.latest_full_frame is None:
            messagebox.showwarning("Notice", "No face detected in camera view yet. Please face the camera.", parent=self)
            return
        self.trigger_snapshot(self.latest_full_frame, self.latest_detected_crop, source="Manual")

    def trigger_snapshot(self, full_frame: np.ndarray, face_crop: np.ndarray, source: str = "Auto"):
        """Freeze frame on captured photo and activate Confirm & Save."""
        self.is_captured = True
        self.captured_crop = face_crop.copy()

        # Render frozen snapshot with green approval border
        display_frame = full_frame.copy()
        h, w, _ = display_frame.shape
        cv2.rectangle(display_frame, (8, 8), (w - 8, h - 8), (0, 255, 0), 6)
        cv2.putText(
            display_frame, f"PHOTO CAPTURED ({source.upper()}) - CLICK CONFIRM TO SAVE",
            (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2
        )

        self.captured_photo_img = image_utils.cv2_to_photoimage(display_frame, (800, 480))
        self.cam_lbl.config(image=self.captured_photo_img)
        self.cam_lbl.image = self.captured_photo_img

        # Update Top Banner
        self.guide_banner.config(
            text="✓ PHOTO CAPTURED! Review above. Click 'Confirm & Save Photo' or 'Retake'.",
            bg=THEME_SUCCESS
        )

        # Hide manual button, show Confirm (Green) & Retake (Orange)
        self.manual_snap_btn.pack_forget()
        self.confirm_btn.config(
            text="✓ Confirm & Save Photo",
            state=tk.NORMAL,
            bg=THEME_SUCCESS
        )
        self.retake_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=15)

    def reset_to_live(self):
        """Reset capture state and resume live camera feed."""
        self.is_captured = False
        self.captured_crop = None
        self.captured_photo_img = None
        self.stable_frames = 0

        self.retake_btn.pack_forget()
        self.manual_snap_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=15)
        self.confirm_btn.config(
            text="Align Face to Auto-Capture",
            state=tk.DISABLED,
            bg="#555555"
        )
        self.guide_banner.config(text="Align your face inside the guide oval...", bg=THEME_WARNING)

        # Resume loop
        self.process_video_loop()

    def save_and_finish(self):
        """Confirm and commit the captured photo into student directory & database."""
        if self.captured_crop is None or self.captured_crop.size == 0:
            messagebox.showerror("Error", "No captured photo available.", parent=self)
            return

        try:
            # 1. Save standardized photo and extract 512-d embedding
            success, photo_path, embedding = face_enrollment_service.save_enrolled_photo(
                self.student_id, self.captured_crop
            )

            # 2. Update Student database record
            rel_photo_path = f"data/students/{self.student_id}.jpg"
            db.execute(
                "UPDATE students SET photo_path = %s, face_embedding = %s WHERE student_id = %s",
                (rel_photo_path, embedding.tobytes(), self.student_id)
            )

            messagebox.showinfo(
                "Enrollment Successful",
                f"Face photo enrolled successfully for {self.student_name}!\n"
                f"Saved to: {photo_path}\n"
                f"Feature vector (512-D) stored in database.",
                parent=self
            )
            self.on_enrolled_callback(rel_photo_path)
            self.on_close()

        except Exception as e:
            logger.error(f"Error during enrollment save: {e}")
            messagebox.showerror("Enrollment Error", f"Failed to save photo: {e}", parent=self)

    def on_close(self):
        """Cleanly release camera on exit."""
        self.is_running = False
        self.is_captured = False
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
        self.destroy()
