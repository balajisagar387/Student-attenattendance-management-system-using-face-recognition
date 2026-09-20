# SOP-06: Attendance Scanner Operations

## 1. Purpose
This SOP details the standard operating procedures for operating the live real-time face recognition scanner during daily classroom or campus entry.

---

## 2. Scanner Mechanics & Optimization

### 2.1 In-Memory Pre-Caching (Eliminating Database Bottleneck)
In the legacy implementation, an SQL connection and multiple queries were executed *inside the video loop for every detected face*, crippling video performance.

In the modernized system:
- When the Scanner opens, all enrolled student metadata and 512-d feature vectors are loaded **once** into high-speed RAM matrix memory.
- During camera processing, face feature matching runs entirely in memory via vector dot-products in $<15$ milliseconds.
- Database write operations occur **only** when a valid student match is newly confirmed, and are debounced to prevent duplicate writes.

### 2.2 Cooldown & Duplicate Prevention
- To prevent a student from having attendance recorded 50 times while standing in front of the camera, the system enforces a **daily duplicate filter**:
  - If Student ID `X` has already been marked *Present* on date `DD/MM/YYYY`, subsequent detections will still highlight their name on screen with an indicator: *(Already Marked Present Today)* without creating redundant database entries.

---

## 3. Daily Operation Procedure

### Step 1: Pre-Session Setup
1. Mount the webcam at eye level near the classroom or hall entrance.
2. Ensure overhead lighting is even; avoid strong direct backlighting (e.g. bright open windows directly behind students).
3. Connect the camera USB cable securely.

### Step 2: Launch the Scanner
1. Log into the application.
2. From the Main Dashboard, click **"Live Attendance Scanner"**.
3. The video stream will start automatically at 30–60 FPS.
4. An on-screen status banner displays:
   - *Total Enrolled Students in Memory*
   - *Current Active Date & Time*
   - *Attendance Log Count for Today*

### Step 3: Student Recognition
1. Students walk past or pause momentarily 0.5 to 1.5 meters from the camera.
2. When a face is detected:
   - A **Green Bounding Box** appears with: `Name | Roll No | Dept | Match %`.
   - The attendance record is instantly written to the database and CSV log.
   - An audible chime confirmation sounds (if audio enabled).
3. If an unrecognized person is in frame:
   - A **Red Bounding Box** appears labeled: `Unknown Face`.
   - No attendance is logged.

### Step 4: Closing the Session
1. Press the on-screen **"Stop Scanner / Back"** button or press the `ESC` / `Enter` key.
2. The camera releases cleanly.
3. The dashboard displays the updated count of students marked present today.
