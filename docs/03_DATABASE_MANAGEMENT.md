# SOP-03: Database Management (SQLite & MySQL)

## 1. Overview
The application supports a dual-mode database architecture designed to provide zero-friction local development and offline operations (via **SQLite**) while offering enterprise scalability and multi-terminal sync (via **MySQL**).

---

## 2. Database Schema Definitions

### 2.1 Table: `users` (Staff & Admin Accounts)
Stores credentials for administrative and faculty operators who can log into the system.

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- INT AUTO_INCREMENT in MySQL
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    security_question VARCHAR(200) NOT NULL,
    security_answer_hash VARCHAR(256) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.2 Table: `students` (Enrolled Student Directory)
Stores student academic information and references to their facial feature data.

```sql
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(50) PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    course VARCHAR(50) NOT NULL,
    year VARCHAR(20) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    division VARCHAR(20),
    roll_no VARCHAR(50) NOT NULL,
    gender VARCHAR(20),
    dob VARCHAR(30),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    teacher VARCHAR(100),
    photo_path VARCHAR(255),
    face_embedding BLOB,                 -- 512-float binary vector for deep matching
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.3 Table: `attendance` (Attendance Logs)
Records real-time detection events.

```sql
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id VARCHAR(50) NOT NULL,
    roll_no VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    log_time VARCHAR(20) NOT NULL,       -- HH:MM:SS
    log_date VARCHAR(20) NOT NULL,       -- DD/MM/YYYY
    status VARCHAR(20) DEFAULT 'Present',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. Switching Between SQLite and MySQL

Configuration is managed entirely through the `.env` file without modifying Python source code.

### Mode A: Embedded SQLite (Default Zero-Config)
In `.env`:
```ini
DB_TYPE=sqlite
SQLITE_PATH=data/attendance_system.db
```
- Requires no database server installation.
- Self-contained file inside `data/`.
- Perfect for single-laptop usage, offline classrooms, and development.

### Mode B: Enterprise MySQL Server
In `.env`:
```ini
DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=student_management
```
- To initialize on MySQL, simply create the empty database once:
  ```sql
  CREATE DATABASE student_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```
- The application automatically builds all required tables upon first launch.

---

## 4. Backup & Maintenance Routines

### 4.1 SQLite Backup
Backing up SQLite requires copying the database file:
```powershell
Copy-Item data/attendance_system.db "backups/attendance_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
```

### 4.2 MySQL Backup
Using `mysqldump`:
```bash
mysqldump -u root -p student_management > backups/mysql_backup_$(date +%Y%m%d).sql
```

### 4.3 Database Optimization
Over time, as hundreds of attendance entries are recorded, run:
- **SQLite**: Execute `VACUUM;` periodically.
- **MySQL**: Execute `OPTIMIZE TABLE attendance;`.
