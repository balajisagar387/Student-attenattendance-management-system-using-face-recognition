# SOP-05: Student Enrollment & Real-Time Pose Guidance

## 1. Purpose
Because the modernized system uses deep 512-dimensional facial embeddings, **only 1 clear reference photo per student is required**. This SOP defines the enrollment procedure and explains the interactive real-time pose guidance system that ensures this single photo is optimal.

---

## 2. Real-Time Pose Guidance Logic

During photo capture, **Google MediaPipe Face Mesh** continuously tracks 468 facial landmark coordinates to assess the student's face orientation and framing:

```
                  PITCH (Up / Down)
                         ▲
                         │
     YAW (Left) ◄─────── ┼ ───────► YAW (Right)
                         │
                         ▼
```

### Guidance Metrics & Criteria

| Check Type | Target Range | Visual Feedback if Failed | Action Required by Student |
| :--- | :--- | :--- | :--- |
| **Yaw (Horizontal Turn)** | Between $-10^\circ$ and $+10^\circ$ | ⚠️ *"Turn head to face the camera"* / *"Looking too far left/right"* | Rotate face to point directly toward the lens. |
| **Pitch (Vertical Tilt)** | Between $-10^\circ$ and $+10^\circ$ | ⚠️ *"Hold head level - do not tilt up/down"* | Keep chin parallel to the ground. |
| **Roll (Sideways Slant)**| Between $-8^\circ$ and $+8^\circ$ | ⚠️ *"Keep head straight - do not tilt sideways"* | Align ears horizontally. |
| **Bounding Scale** | 35% to 55% of video frame height | ⚠️ *"Move closer"* or *"Step back"* | Adjust physical distance to be ~50–80 cm from the camera. |
| **Centering** | Within center 30% oval of frame | ⚠️ *"Center your face in the oval guide"* | Align face inside the on-screen guideline. |
| **Lighting / Clarity** | Laplacian variance $> 80$ | ⚠️ *"Hold still, image blurry"* / *"Low lighting"* | Avoid rapid movement; ensure face is illuminated. |

---

## 3. Interactive Guide Overlay States

The camera view renders an interactive targeting reticle with live dynamic color-coding:

- **🔴 Red Outline**: Face not detected, multiple faces in frame, or severe misalignment.
- **🟡 Yellow Outline**: Face detected but outside pose tolerance (e.g. tilted head, too far). On-screen text directs the user on how to correct the pose.
- **🟢 Green Outline**: **Perfect Alignment!** All thresholds satisfied. The **"Capture Photo"** button unlocks, and a 1-second countdown timer initiates automatic snapshot capture.

---

## 4. Step-by-Step Enrollment Procedure

### Step 1: Open Student Management
1. Log in to the application and navigate to **Student Management**.
2. Click **"Add New Student"** or select an existing record to update.
3. Fill in academic details:
   - **Department** (Computer, IT, Civil, Mechanical, etc.)
   - **Course** (B.Tech, M.Tech, BE, BCA, MCA, etc.)
   - **Year & Semester**
   - **Student ID** (Must be unique, e.g. `2024CS001`)
   - **Student Name**, **Roll Number**, **Gender**, **DOB**
   - **Contact Email**, **Phone Number**, **Address**
4. Click **"Save Details"**.

### Step 2: Launch Guided Photo Enrollment
1. Click **"Capture Face Photo"** on the student form.
2. The interactive camera enrollment window will open.
3. Have the student stand or sit comfortably 50–80 cm from the webcam.
4. Observe the on-screen feedback:
   - If the banner says *"Look straight"*, prompt the student to align with the camera.
   - If the banner says *"Move closer"*, have them lean slightly forward until the face fills the oval guide.
5. Once the oval turns **Green**, click **"Capture & Enroll"** (or let auto-capture complete).
6. The system crops the normalized face, calculates the 512-dimensional embedding, and saves the image to:
   `data/students/{student_id}.jpg`
7. A confirmation dialog will report: *"Face photo and embedding enrolled successfully!"*
