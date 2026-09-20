# SOP-07: Reporting, Analytics & Data Export

## 1. Purpose
This SOP guides administrative and academic personnel on querying, auditing, manually correcting, and exporting daily and monthly attendance reports.

---

## 2. Viewing Attendance Records
1. From the Main Dashboard, click **"Attendance Records"**.
2. The Attendance Table displays:
   - `Attendance ID`: Unique tracking sequence number.
   - `Student ID`: Unique student identification key.
   - `Roll No`: Class roll number.
   - `Name`: Full student name.
   - `Department`: Academic department (e.g. IT, Computer, Civil).
   - `Time`: Exact capture timestamp (`HH:MM:SS`).
   - `Date`: Record date (`DD/MM/YYYY`).
   - `Status`: `Present`, `Late`, or `Excused`.

---

## 3. Filtering and Searching Records
The search bar allows rapid lookup by:
- **Search by Date**: Filter attendance for a specific day or date range.
- **Search by Department**: Review all attendance logs for a particular branch.
- **Search by Student ID or Roll No**: Review an individual student's log history.

---

## 4. Manual Record Adjustments
If a student was unable to scan due to an injury or technical issue, operators can record attendance manually:
1. Select the student record or enter their Student ID in the attendance form.
2. Verify the auto-populated Department and Name.
3. Select status as **"Present"** or **"Excused"**.
4. Click **"Save / Update Attendance"**.

To remove an incorrect log:
1. Select the entry in the table.
2. Click **"Delete Record"** and confirm the prompt.

---

## 5. Exporting to CSV & Excel

### Standard CSV Export Routine
1. In the Attendance Records screen, apply any desired filters (e.g. select today's date).
2. Click **"Export CSV"**.
3. A system save dialog opens with a pre-formatted filename:
   `attendance_report_YYYY-MM-DD.csv`
4. Choose destination folder and click **Save**.
5. The generated CSV is directly compatible with Microsoft Excel, Google Sheets, and institutional ERP systems.

### Automated Daily CSV Mirroring
In addition to on-demand export, the application automatically mirrors all live scan detections into daily audit logs located at:
`data/attendance/attendance_YYYY-MM-DD.csv`
This ensures zero data loss even if power is abruptly lost or the database connection drops.
