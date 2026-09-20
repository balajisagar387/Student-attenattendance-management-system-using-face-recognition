# SOP-02: Installation & Environment Setup

## 1. Purpose
This procedure defines the end-to-end setup of the runtime environment, dependencies, hardware permissions, and initial configuration across Windows, macOS, and Linux.

---

## 2. Prerequisites & System Requirements

### Hardware Requirements
- **CPU**: Intel Core i3 / AMD Ryzen 3 or higher (AVX2 support recommended).
- **RAM**: 4 GB minimum (8 GB recommended).
- **Camera**: Standard USB 720p/1080p webcam or built-in laptop webcam.
- **Disk Space**: 500 MB free space for code, dependencies, and student photos.

### Software Requirements
- **Python**: 3.9, 3.10, 3.11, or 3.12 (64-bit recommended).
- **Git**: Installed and available on system PATH.

---

## 3. Step-by-Step Installation

### Step 1: Open Terminal in Project Directory
Navigate to the root folder of the project:
```powershell
cd "student management system"
```

### Step 2: Create a Clean Virtual Environment
Always install dependencies inside an isolated virtual environment to prevent package version conflicts:
```powershell
# Create virtual environment named 'venv'
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt)
.\venv\Scripts\activate.bat

# Activate on macOS / Linux
source venv/bin/activate
```

### Step 3: Upgrade Pip & Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Settings
Create your active `.env` configuration file from the template:
```powershell
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

Review `.env` settings:
- By default, `DB_TYPE=sqlite` is enabled for zero-setup local operation.
- If you have an existing MySQL server, adjust `DB_TYPE=mysql` and supply your host, port, username, and password.

---

## 4. Hardware Verification (Camera Access)

1. Ensure your webcam is connected and recognized by Windows (`Device Manager -> Cameras`).
2. If using Windows 10/11, ensure camera privacy permissions allow desktop applications:
   - Go to: **Windows Settings -> Privacy & Security -> Camera**.
   - Ensure **"Let desktop apps access your camera"** is turned **ON**.
3. In `.env`, `CAMERA_INDEX=0` selects the default primary webcam. If you have multiple cameras (e.g. external USB camera), change this to `1` or `2`.

---

## 5. Launching the Application
Execute the primary runner script:
```powershell
python run.py
```
Upon the first run:
- The database schema is automatically verified and initialized.
- Default storage folders (`data/students/`, `data/attendance/`) are verified or created.
- The login window will appear.
