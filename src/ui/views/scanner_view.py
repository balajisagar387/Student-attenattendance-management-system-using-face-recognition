"""Live Real-Time Face Recognition Attendance Scanner View."""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any, List
from datetime import datetime
import cv2
import numpy as np
from config.settings import settings
from src.core.logger import logger
from src.services.pose_estimator import pose_estimator
from src.services.face_recognizer import face_recognizer_service
from src.services.attendance_service import attendance_service
from src.utils.image_utils import image_utils
from src.ui.styles import *

class ScannerView(tk.Frame):
    def __init__(self, master, navigate_to: Callable[[str], None]):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self.navigate_to = navigate_to
        self.cap = None
        self.is_running = False
        self.session_marked: List[Dict[str, Any]] = []

        self.build_ui()
        self.start_scanner()

    def build_ui(self):
        # 1. Header Bar
        header = tk.Frame(self, bg=BG_CARD, height=60, padx=25)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title = tk.Label(header, text="Live AI Face Recognition Scanner", font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
        title.pack(side=tk.LEFT, pady=15)

        self.status_tag = tk.Label(header, text="STATUS: INITIALIZING...", font=FONT_SMALL, fg=THEME_WARNING, bg=BG_CARD)
        self.status_tag.pack(side=tk.LEFT, padx=20, pady=18)

        back_btn = tk.Button(header, text="Stop Scanner / Dashboard", font=FONT_BODY, bg=THEME_DANGER, fg=TEXT_PRIMARY,
                             bd=0, cursor="hand2", padx=15, pady=4, command=self.stop_and_exit)
        back_btn.pack(side=tk.RIGHT, pady=15)

        # 2. Main Body Split (Left: Camera Feed, Right: Live Activity Log)
        body = tk.Frame(self, bg=BG_DARK, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        # Camera View Card
        cam_card = tk.Frame(body, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=15, pady=15)
        cam_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        self.cam_lbl = tk.Label(cam_card, bg="#000000")
        self.cam_lbl.pack(fill=tk.BOTH, expand=True)

        # Right Panel: Real-time Detections & Activity
        right_panel = tk.Frame(body, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=20, pady=20, width=380)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="Today's Live Detections", font=FONT_BODY_BOLD, fg=TEXT_PRIMARY, bg=BG_CARD).pack(anchor="w", pady=(0, 10))

        # Recent activity treeview
        columns = ("time", "name", "status")
        self.activity_tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=15)
        self.activity_tree.heading("time", text="Time")
        self.activity_tree.heading("name", text="Student Name")
        self.activity_tree.heading("status", text="Status")

        self.activity_tree.column("time", width=80)
        self.activity_tree.column("name", width=140)
        self.activity_tree.column("status", width=90)
        self.activity_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Live Summary Card
        summary_card = tk.Frame(right_panel, bg=BG_CARD_LIGHT, padx=15, pady=12, bd=1, relief=tk.SOLID)
        summary_card.pack(fill=tk.X, side=tk.BOTTOM)

        self.cached_count_lbl = tk.Label(
            summary_card,
            text=f"Loaded Enrolled Vectors: {len(face_recognizer_service.enrolled_cache)}",
            font=FONT_SMALL, fg=THEME_SUCCESS, bg=BG_CARD_LIGHT
        )
        self.cached_count_lbl.pack(anchor="w")

        self.total_marked_lbl = tk.Label(
            summary_card, text="Marked This Session: 0", font=FONT_SMALL, fg=TEXT_PRIMARY, bg=BG_CARD_LIGHT
        )
        self.total_marked_lbl.pack(anchor="w", pady=(4, 0))

    def start_scanner(self):
        """Start live webcam processing."""
        face_recognizer_service.reload_enrolled_cache()
        self.cached_count_lbl.config(text=f"Loaded Enrolled Vectors: {len(face_recognizer_service.enrolled_cache)}")

        try:
            self.cap = cv2.VideoCapture(settings.CAMERA_INDEX)
            if not self.cap.isOpened():
                self.status_tag.config(text="STATUS: CAMERA ERROR", fg=THEME_DANGER)
                messagebox.showerror("Camera Error", "Could not connect to webcam.", parent=self.master)
                return
            self.is_running = True
            self.status_tag.config(text="STATUS: LIVE SCANNING (30-60 FPS)", fg=THEME_SUCCESS)
            self.process_scanner_tick()
        except Exception as e:
            logger.error(f"Error starting scanner: {e}")
            self.status_tag.config(text="STATUS: FAILED", fg=THEME_DANGER)

    def process_scanner_tick(self):
        """Single tick of real-time camera loop."""
        if not self.is_running or not self.cap:
            return

        ret, frame = self.cap.read()
        if ret and frame is not None:
            frame = cv2.flip(frame, 1)

            # Evaluate face detection
            eval_res = pose_estimator.evaluate_frame(frame)
            box = eval_res.get("box")
            crop = eval_res.get("crop")

            if eval_res.get("face_detected") and crop is not None and crop.size > 0:
                is_match, candidate, confidence = face_recognizer_service.recognize_face(crop)

                if is_match and candidate:
                    # Recognized Student
                    name = candidate["name"]
                    roll = candidate["roll_no"]
                    s_id = candidate["student_id"]
                    dept = candidate["department"]
                    conf_pct = int(confidence * 100)

                    color = (0, 255, 0) # Green
                    label = f"{name} ({roll}) | {conf_pct}%"

                    # Record attendance with debounce protection
                    if face_recognizer_service.should_record_attendance(s_id):
                        recorded = attendance_service.mark_attendance(s_id, roll, name, dept)
                        now_str = datetime.now().strftime("%H:%M:%S")
                        status_str = "Logged" if recorded else "Already Present"

                        self.activity_tree.insert("", 0, values=(now_str, name, status_str))
                        if recorded:
                            self.session_marked.append(candidate)
                            self.total_marked_lbl.config(text=f"Marked This Session: {len(self.session_marked)}")
                else:
                    color = (0, 0, 255) # Red
                    label = "Unknown Face"

                if box:
                    x, y, w, h = box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

            photo = image_utils.cv2_to_photoimage(frame, (760, 520))
            self.cam_lbl.config(image=photo)
            self.cam_lbl.image = photo

        self.after(25, self.process_scanner_tick)

    def stop_and_exit(self):
        """Release camera and return to dashboard."""
        self.is_running = False
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
        self.navigate_to("dashboard")
