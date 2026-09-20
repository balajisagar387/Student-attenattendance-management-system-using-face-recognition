# SOP-04: Security & User Access Management

## 1. Purpose
This procedure defines policies, credential safeguards, role access, and password recovery mechanisms for the attendance management system.

---

## 2. Cryptographic Security Standards

### 2.1 Elimination of Plaintext Passwords
In the legacy codebase, user passwords and security answers were stored as plaintext in MySQL tables. 

In the modernized system:
- All passwords and security answers are processed through cryptographic key derivation functions:
  $$\text{Hash} = \text{PBKDF2-HMAC-SHA256}(\text{Password}, \text{Salt}, \text{100,000 Iterations})$$
- Each user account has a unique randomly generated 16-byte cryptographic salt.
- The salt and derived digest are stored in the database in standard modular format (`algorithm$iterations$salt$hash`).
- Plaintext passwords never touch logs, console outputs, or persistent storage.

### 2.2 Removal of Hardcoded Backdoor Accounts
The hardcoded credentials (`bala` / `bala`) present in the legacy `login.py` script have been completely eliminated. Access requires an authenticated record in the `users` table.

---

## 3. User Registration Standard Operating Procedure

1. Launch the application via `python run.py`.
2. On the Login Screen, click **"New User Register"**.
3. Enter required fields:
   - **First Name & Last Name**: Alphabetic characters only.
   - **Contact Number**: Exactly 10 digits.
   - **Email Address**: Valid email format containing `@` and valid domain.
   - **Security Question**: Select one from the pre-defined dropdown:
     - *What is your birth city?*
     - *What was the name of your first school?*
     - *What is your favorite book?*
     - *What is your mother's maiden name?*
   - **Security Answer**: Case-insensitive answer hashed upon submission.
   - **Password & Confirm Password**: Minimum 6 characters (mix of alphanumeric recommended).
4. Review and check **"I agree to the Terms & Conditions"**.
5. Click **"Register"**. Upon confirmation, the account is activated immediately.

---

## 4. Password Recovery (Forgot Password Workflow)

If an authorized user forgets their password:
1. On the Login Screen, click **"Forgot Password"**.
2. Enter the registered **Email Address** and click **"Verify Email"**.
3. The system will retrieve the assigned security question.
4. Provide the exact **Security Answer** set during registration.
5. Enter the **New Password** and confirm.
6. Click **"Reset Password"**. If the security answer matches, the password hash is updated immediately.

---

## 5. Security Checklist for System Administrators

- [x] Change all default MySQL root passwords from `balu123` to a secure enterprise password.
- [x] Ensure the `.env` file is excluded from public Git repositories (enforced via `.gitignore`).
- [x] Rotate admin credentials every 90 days.
- [x] Restrict physical access to the attendance kiosk terminal.
