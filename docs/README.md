# Standard Operating Procedures (SOPs) & Documentation

Welcome to the official documentation and management guidelines for the **Next-Gen Student Attendance Management System**.

This directory contains standardized, step-by-step procedures for administrators, IT staff, and operators to install, configure, operate, and maintain the application.

---

## Documentation Index

| Doc ID | Standard Operating Procedure | Target Audience | Description |
| :--- | :--- | :--- | :--- |
| **[SOP-01](01_SYSTEM_ARCHITECTURE.md)** | **System Architecture & Design** | Developers, Architects | Detailed system overview, component data flow, and modern tech stack. |
| **[SOP-02](02_INSTALLATION_AND_SETUP.md)** | **Installation & Environment Setup** | IT Admins, Developers | Step-by-step setup on Windows, macOS, and Linux; virtual environments and camera access. |
| **[SOP-03](03_DATABASE_MANAGEMENT.md)** | **Database Management (SQLite & MySQL)** | DBAs, IT Admins | Dual-mode configuration, table schema definitions, migrations, backup, and restore routines. |
| **[SOP-04](04_SECURITY_AND_USER_ACCESS.md)** | **Security & User Access Management** | System Admins | Staff registration, salted cryptographic password hashing, role permissions, and password recovery. |
| **[SOP-05](05_STUDENT_ENROLLMENT_GUIDELINES.md)** | **Student Enrollment & Pose Guidance** | Teachers, Lab Operators | Best practices for capturing the single high-quality reference photo using real-time MediaPipe pose feedback. |
| **[SOP-06](06_ATTENDANCE_SCANNER_OPERATIONS.md)** | **Attendance Scanner Operations** | Daily Operators, Faculty | How to launch and run the live face recognition scanner, adjust thresholds, and handle live matching. |
| **[SOP-07](07_REPORTING_AND_DATA_EXPORT.md)** | **Reporting, Analytics & Data Export** | Admin, Office Staff | Querying attendance records, generating daily/monthly CSV logs, and performing manual adjustments. |
| **[SOP-08](08_TROUBLESHOOTING_AND_FAQ.md)** | **Troubleshooting, Diagnostics & FAQ** | All Users, IT Support | Resolving common issues: webcam index errors, lighting warnings, database locks, and performance tuning. |

---

## Quick Reference Summary

- **Primary Launcher**: `python run.py`
- **Configuration File**: `.env` (copied from `.env.example`)
- **Default Database**: Embedded SQLite (`data/attendance_system.db`) — zero server installation needed.
- **Enterprise Database**: MySQL (configured in `.env` via `DB_TYPE=mysql`).
- **Student Photos**: Stored in `data/students/` indexed by Student ID.
- **Attendance Exports**: Auto-saved to `data/attendance/`.
