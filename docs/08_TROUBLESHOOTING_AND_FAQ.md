# SOP-08: Troubleshooting, Diagnostics & FAQ

## 1. Diagnostic Matrix & Common Errors

| Symptom / Error | Root Cause | Resolution Procedure |
| :--- | :--- | :--- |
| **`cv2.VideoCapture: Camera index out of range`** | The webcam is unplugged, in use by another app (e.g. Zoom/Teams), or camera index is incorrect. | 1. Close any video conferencing software.<br>2. Check USB cable connection.<br>3. In `.env`, change `CAMERA_INDEX=0` to `CAMERA_INDEX=1`. |
| **`AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'`** | Using modern Pillow (>= 10.0.0) with legacy code. | The modernized codebase replaces all `ANTIALIAS` with `Image.Resampling.LANCZOS`. If seeing this, ensure running from `python run.py`. |
| **`Can't connect to MySQL server on 'localhost'`** | MySQL service is stopped or port 3306 is blocked. | 1. Start MySQL service via Windows Services (`services.msc`) or XAMPP.<br>2. Or switch to offline zero-config SQLite mode: set `DB_TYPE=sqlite` in `.env`. |
| **Enrollment: Banner persistently shows *"Low Lighting / Blurry"*** | Room is too dark or camera focus is blurred. | 1. Turn on classroom overhead lights.<br>2. Clean the camera lens with a microfiber cloth.<br>3. Ensure student remains still for 1 second. |
| **Scanner: High false *"Unknown Face"* detections** | Match confidence threshold is set too conservatively, or student photo was captured poorly. | 1. In `.env`, adjust `CONFIDENCE_THRESHOLD=0.55` (default is 0.60).<br>2. Re-enroll the student under clean lighting following [SOP-05](05_STUDENT_ENROLLMENT_GUIDELINES.md). |
| **Database is locked (`sqlite3.OperationalError: database is locked`)** | Another process has opened the SQLite file for writing. | Close external SQLite viewers (e.g. DB Browser for SQLite) or restart the application. |

---

## 2. Frequently Asked Questions (FAQ)

### Q1: Can I run this system without internet access?
**Yes, absolutely.** Both Google MediaPipe and the deep embedding models run 100% locally on your machine's CPU. No cloud API or active internet connection is required once initial pip packages are installed.

### Q2: Do I have to install MySQL to use this app?
**No.** By default, the system uses embedded SQLite (`data/attendance_system.db`). It works instantly out-of-the-box. If your institution uses a central MySQL server, you can switch simply by editing `.env`.

### Q3: What happens if a student wears glasses or changes their hairstyle?
Deep learning feature embeddings are largely invariant to minor cosmetic changes (hairstyles, light makeup, prescription glasses). For best results, capture the student wearing their everyday glasses during enrollment.

### Q4: Can two people be recognized simultaneously?
**Yes.** MediaPipe detects all faces in the camera frame simultaneously, and the recognition engine loops through each face in under 15 milliseconds, displaying bounding boxes and names for all detected students.

### Q5: How do I move the application to another computer?
1. Copy the entire project directory to the new computer.
2. Install Python 3.10+ and run `pip install -r requirements.txt`.
3. Copy the `data/` folder (which contains the SQLite database and enrolled student photos).
4. Run `python run.py`. Everything will resume with all student records intact.
