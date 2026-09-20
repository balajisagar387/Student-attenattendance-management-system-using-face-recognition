# SOP-01: System Architecture & Design

## 1. Overview
The **Next-Gen Student Attendance Management System** is an AI-powered desktop application engineered to automate classroom attendance using computer vision. It detects student faces in real-time, matches them against pre-enrolled facial feature vectors (embeddings), and automatically records attendance timestamps into a persistent relational database and daily CSV audits.

---

## 2. High-Level Architecture Diagram

```
+-------------------------------------------------------------------------------+
|                               Presentation Layer                              |
|                       (CustomTkinter Modern Desktop UI)                       |
|   +---------------+  +---------------+  +---------------+  +---------------+  |
|   |  Login / Auth |  |   Dashboard   |  | Student Mgmt  |  |  Live Scanner |  |
|   +-------+-------+  +-------+-------+  +-------+-------+  +-------+-------+  |
+-----------|------------------|------------------|------------------|----------+
            |                  |                  |                  |
+-----------v------------------v------------------v------------------v----------+
|                                 Service Layer                                 |
|  +--------------------+  +--------------------+  +-------------------------+  |
|  |    AuthService     |  |   StudentService   |  |    AttendanceService    |  |
|  +--------------------+  +--------------------+  +-------------------------+  |
|  +--------------------+  +--------------------+  +-------------------------+  |
|  | PoseEstimator (MP) |  |   FaceEnrollment   |  | FaceRecognizer (Insight)|  |
|  +--------------------+  +--------------------+  +-------------------------+  |
+-----------|--------------------------------------------------------|----------+
            |                                                        |
+-----------v--------------------------------------------------------v----------+
|                             Core & Infrastructure                             |
|  +-----------------------+  +----------------------+  +--------------------+  |
|  | Database Manager (DB) |  |   Security Module    |  |  Settings Manager  |  |
|  +-----------+-----------+  +----------------------+  +--------------------+  |
+--------------|----------------------------------------------------------------+
               |
+--------------v----------------------------------------------------------------+
|                               Persistence Layer                               |
|        [ SQLite (Default Local) ]     OR     [ MySQL (Enterprise Server) ]     |
|        [ CSV Audit Files ]                   [ Enrolled Reference Images ]    |
+-------------------------------------------------------------------------------+
```

---

## 3. Component Breakdown

### 3.1 Presentation Layer (`src/ui/`)
- Built using **CustomTkinter** for high-DPI awareness, consistent typography, smooth animations, and automatic dark/light theme adaptation.
- Divided into independent modular views (`login_view.py`, `dashboard_view.py`, `student_view.py`, `enrollment_view.py`, `scanner_view.py`, `attendance_view.py`).

### 3.2 Computer Vision Pipeline (`src/services/`)
- **Detection & Pose Estimation (`pose_estimator.py`)**: Powered by **Google MediaPipe BlazeFace**. Evaluates 468 landmark points in real-time ($<5$ ms per frame) to compute:
  - **Yaw (Left/Right turn)**: Target $\pm 10^\circ$.
  - **Pitch (Up/Down tilt)**: Target $\pm 10^\circ$.
  - **Roll (Sideways slant)**: Target $\pm 8^\circ$.
  - **Scale/Framing**: Confirms head occupies 35%–55% of the detection frame.
- **Deep Feature Recognition (`face_recognizer.py`)**: Uses **InsightFace ONNX** models to extract 512-dimensional vector embeddings. Recognition is computed via normalized cosine distance against enrolled student vectors.

### 3.3 Data Access Layer (`src/core/db.py`)
- Provides a unified abstraction layer over **SQLite** and **MySQL**.
- Employs parameter binding across all operations to prevent SQL injection vulnerabilities.
- Handles automated schema generation on application startup.

---

## 4. Key Improvements over Legacy System

| Feature | Legacy 2022 Implementation | Modernized Architecture |
| :--- | :--- | :--- |
| **Photos Needed** | 150 webcam frames per student | **Exactly 1 high-quality photo** |
| **Model Retraining** | Required rebuilding a 40MB XML file whenever student added | **Zero retraining** — vectors added dynamically |
| **Face Orientation** | Fails on slight head turn or angle | **Real-time 3D pose guidance overlay** |
| **Database Connection**| Opened per detected face per video frame | **Pre-cached student memory index + persistent connection pool** |
| **UI Responsiveness** | UI froze completely during camera scan | **Background thread camera pump** |
| **Security** | Plain-text passwords, hardcoded credentials | **Salted cryptographic hashes, zero plaintext storage** |
