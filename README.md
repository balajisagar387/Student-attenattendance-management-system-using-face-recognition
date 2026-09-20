# Student Attendance Management System (AI Face Recognition)

A modern, high-performance desktop application for student attendance management powered by **Google MediaPipe** face pose guidance, **Deep Learning Face Embeddings**, and a **Dual SQLite / MySQL Database Architecture**.

---

## Key Features

- **Single-Photo Enrollment**: No more capturing 150 photos per student. One crisp frontal photo generates a 512-dimensional vector embedding stored in the database.
- **Real-Time Interactive Pose Guidance**:
  - Live feedback during photo capture: *"Look straight"*, *"Hold head level"*, *"Move closer"*, *"Center your face"*.
  - Visual guidance target reticle changes from Red $\to$ Yellow $\to$ Green when alignment is optimal.
- **Live 60 FPS Face Recognition Scanner**:
  - High-speed vector dot-product matching in memory ($<15$ ms per frame).
  - Green bounding box with student details and match confidence percentage.
  - Automatic duplicate prevention so students are only logged once per calendar day.
- **Dual-Mode Zero-Config Database**:
  - **SQLite (Default)**: Embedded, offline, zero-setup file database in `data/attendance_system.db`.
  - **MySQL (Enterprise)**: Configurable with a single `.env` setting (`DB_TYPE=mysql`) for campus-wide network sync.
- **Cryptographic Security**:
  - Salted PBKDF2-HMAC-SHA256 password hashing.
  - No plaintext credentials; removal of legacy hardcoded backdoor passwords.
- **Full Standard Operating Procedures Suite**: Complete documentation and maintenance SOPs available in [`docs/`](docs/).

---

## Project Structure

```
student management system/
├── .env.example                     # Environment settings template
├── .gitignore                       # Clean git ignore (data, pycache, envs)
├── README.md                        # Project documentation
├── requirements.txt                 # Modern locked dependencies
├── run.py                           # Application entrypoint
│
├── config/                          # Central configuration
│   ├── settings.py                  # Environment settings & dynamic paths
│   └── constants.py                 # Academic lists, colors, guidance messages
│
├── src/                             # Core application package
│   ├── core/                        # Infrastructure
│   │   ├── db.py                    # Unified SQLite/MySQL database manager
│   │   ├── security.py              # Salted password hashing & verification
│   │   └── logger.py                # Centralized application logging
│   │
│   ├── services/                    # Business & Computer Vision logic
│   │   ├── auth_service.py          # User registration & authentication
│   │   ├── student_service.py       # Student CRUD operations
│   │   ├── attendance_service.py    # Attendance logging & CSV export
│   │   ├── pose_estimator.py        # MediaPipe landmark analysis & pose guide
│   │   ├── face_enrollment.py       # Single-photo guided capture service
│   │   └── face_recognizer.py       # Live recognition & attendance pipeline
│   │
│   ├── ui/                          # Presentation layer
│   │   ├── app.py                   # Central window & view router
│   │   ├── styles.py                # Modern styling palette & fonts
│   │   └── views/                   # Modular views
│   │       ├── login_view.py        # Auth & registration
│   │       ├── dashboard_view.py    # Main modern dashboard
│   │       ├── student_view.py      # Student directory & management
│   │       ├── enrollment_view.py   # Guided camera photo capture
│   │       ├── scanner_view.py      # Live face recognition scanner
│   │       ├── attendance_view.py   # Attendance log, search & export
│   │       └── help_view.py         # System info & developer support
│   │
│   └── utils/                       # Shared utilities
│       ├── image_utils.py           # Modern LANCZOS resizing & frame conversion
│       └── validators.py            # Email, phone, and name validation
│
├── data/                            # Dynamic data (git-ignored)
│   ├── students/                    # Enrolled single reference photos
│   └── attendance/                  # Daily attendance CSV reports
│
└── docs/                            # Standard Operating Procedures (SOPs)
    ├── README.md                    # Documentation index
    ├── 01_SYSTEM_ARCHITECTURE.md
    ├── 02_INSTALLATION_AND_SETUP.md
    ├── 03_DATABASE_MANAGEMENT.md
    ├── 04_SECURITY_AND_USER_ACCESS.md
    ├── 05_STUDENT_ENROLLMENT_GUIDELINES.md   # Pose guidance & photo SOP
    ├── 06_ATTENDANCE_SCANNER_OPERATIONS.md  # Live recognition SOP
    ├── 07_REPORTING_AND_DATA_EXPORT.md
    └── 08_TROUBLESHOOTING_AND_FAQ.md
```

---

## Quickstart Guide

### 1. Create Virtual Environment & Install Dependencies
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Environment
```powershell
Copy-Item .env.example .env
```
*(By default, `DB_TYPE=sqlite` requires zero server setup and runs immediately).*

### 3. Launch Application
```powershell
python run.py
```

---

## Standard Operating Procedures (docs/)

Detailed operating procedures are located in the [`docs/`](docs/) directory:
- [SOP-01: System Architecture](docs/01_SYSTEM_ARCHITECTURE.md)
- [SOP-02: Installation & Environment Setup](docs/02_INSTALLATION_AND_SETUP.md)
- [SOP-03: Database Management (SQLite & MySQL)](docs/03_DATABASE_MANAGEMENT.md)
- [SOP-04: Security & User Access](docs/04_SECURITY_AND_USER_ACCESS.md)
- [SOP-05: Student Enrollment & Real-Time Pose Guidance](docs/05_STUDENT_ENROLLMENT_GUIDELINES.md)
- [SOP-06: Attendance Scanner Operations](docs/06_ATTENDANCE_SCANNER_OPERATIONS.md)
- [SOP-07: Reporting, Analytics & Data Export](docs/07_REPORTING_AND_DATA_EXPORT.md)
- [SOP-08: Troubleshooting & FAQ](docs/08_TROUBLESHOOTING_AND_FAQ.md)
