"""Modern Login, Registration, and Password Recovery View."""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
from config.settings import settings
from config.constants import SECURITY_QUESTIONS
from src.core.logger import logger
from src.services.auth_service import auth_service
from src.utils.validators import validators
from src.ui.styles import *

class LoginView(tk.Frame):
    def __init__(self, master, on_login_success: Callable):
        super().__init__(master, bg=BG_DARK)
        self.master = master
        self.on_login_success = on_login_success
        self.build_ui()

    def build_ui(self):
        # Center container card
        card = tk.Frame(self, bg=BG_CARD, bd=1, relief=tk.SOLID, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=420, height=520)

        # App Icon / Header
        title_lbl = tk.Label(card, text="System Login", font=FONT_TITLE, fg=TEXT_PRIMARY, bg=BG_CARD)
        title_lbl.pack(pady=(0, 10))

        subtitle_lbl = tk.Label(card, text="Student Attendance Management", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD)
        subtitle_lbl.pack(pady=(0, 25))

        # Email Field
        tk.Label(card, text="Email Address", font=FONT_BODY_BOLD, fg=TEXT_PRIMARY, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        self.email_entry = tk.Entry(card, font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        self.email_entry.pack(fill=tk.X, pady=(5, 15), ipady=6)

        # Password Field
        tk.Label(card, text="Password", font=FONT_BODY_BOLD, fg=TEXT_PRIMARY, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        self.pass_entry = tk.Entry(card, show="*", font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        self.pass_entry.pack(fill=tk.X, pady=(5, 20), ipady=6)

        # Login Action Button
        login_btn = tk.Button(card, text="Log In", font=FONT_BODY_BOLD, bg=THEME_PRIMARY, fg=TEXT_PRIMARY,
                              activebackground=THEME_HOVER, activeforeground=TEXT_PRIMARY,
                              bd=0, cursor="hand2", command=self.handle_login)
        login_btn.pack(fill=tk.X, ipady=8, pady=(5, 15))

        # Links
        links_frame = tk.Frame(card, bg=BG_CARD)
        links_frame.pack(fill=tk.X, pady=10)

        reg_btn = tk.Button(links_frame, text="Register New User", font=FONT_SMALL, fg=THEME_SUCCESS, bg=BG_CARD,
                            bd=0, cursor="hand2", command=self.open_register_window)
        reg_btn.pack(side=tk.LEFT)

        forgot_btn = tk.Button(links_frame, text="Forgot Password?", font=FONT_SMALL, fg=THEME_WARNING, bg=BG_CARD,
                               bd=0, cursor="hand2", command=self.open_forgot_window)
        forgot_btn.pack(side=tk.RIGHT)

        # Quick tip
        tip_lbl = tk.Label(card, text="Offline Secure Mode Active", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD)
        tip_lbl.pack(side=tk.BOTTOM, pady=(20, 0))

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password.", parent=self.master)
            return

        success, user, msg = auth_service.authenticate(email, password)
        if success:
            logger.info(f"User {email} logged in successfully.")
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", msg, parent=self.master)

    def open_register_window(self):
        win = tk.Toplevel(self.master)
        win.title("User Registration")
        win.geometry("500x620")
        win.configure(bg=BG_DARK)
        win.grab_set()

        card = tk.Frame(win, bg=BG_CARD, padx=30, pady=25)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(card, text="Create New User Account", font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD).pack(pady=(0, 15))

        # Form fields
        fields = {}
        row_fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email Address", "email"),
            ("Contact Number (10 digits)", "phone"),
        ]

        for label_text, key in row_fields:
            tk.Label(card, text=label_text, font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD, anchor="w").pack(fill=tk.X)
            e = tk.Entry(card, font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
            e.pack(fill=tk.X, pady=(2, 8), ipady=4)
            fields[key] = e

        # Security question
        tk.Label(card, text="Security Question", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        q_combo = ttk.Combobox(card, values=SECURITY_QUESTIONS, state="readonly", font=FONT_BODY)
        q_combo.current(0)
        q_combo.pack(fill=tk.X, pady=(2, 8), ipady=2)
        fields["security_question"] = q_combo

        tk.Label(card, text="Security Answer", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        ans_e = tk.Entry(card, font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        ans_e.pack(fill=tk.X, pady=(2, 8), ipady=4)
        fields["security_answer"] = ans_e

        tk.Label(card, text="Password", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        pw_e = tk.Entry(card, show="*", font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        pw_e.pack(fill=tk.X, pady=(2, 8), ipady=4)
        fields["password"] = pw_e

        def submit_reg():
            data = {k: v.get().strip() if hasattr(v, "get") else "" for k, v in fields.items()}
            # Validation
            ok, err = validators.validate_name(data["first_name"], "First Name")
            if not ok:
                messagebox.showerror("Error", err, parent=win)
                return
            ok, err = validators.validate_name(data["last_name"], "Last Name")
            if not ok:
                messagebox.showerror("Error", err, parent=win)
                return
            ok, err = validators.validate_email(data["email"])
            if not ok:
                messagebox.showerror("Error", err, parent=win)
                return
            ok, err = validators.validate_phone(data["phone"])
            if not ok:
                messagebox.showerror("Error", err, parent=win)
                return
            if len(data["password"]) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters.", parent=win)
                return
            if not data["security_answer"]:
                messagebox.showerror("Error", "Please provide an answer to the security question.", parent=win)
                return

            succ, msg = auth_service.register_user(data)
            if succ:
                messagebox.showinfo("Success", "Account created successfully! You can now log in.", parent=win)
                win.destroy()
            else:
                messagebox.showerror("Error", msg, parent=win)

        tk.Button(card, text="Register Account", font=FONT_BODY_BOLD, bg=THEME_SUCCESS, fg=TEXT_PRIMARY,
                  bd=0, cursor="hand2", command=submit_reg).pack(fill=tk.X, pady=(15, 0), ipady=6)

    def open_forgot_window(self):
        win = tk.Toplevel(self.master)
        win.title("Reset Password")
        win.geometry("450x450")
        win.configure(bg=BG_DARK)
        win.grab_set()

        card = tk.Frame(win, bg=BG_CARD, padx=30, pady=25)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(card, text="Password Recovery", font=FONT_SUBTITLE, fg=TEXT_PRIMARY, bg=BG_CARD).pack(pady=(0, 15))

        tk.Label(card, text="Enter Registered Email", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        email_e = tk.Entry(card, font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        email_e.pack(fill=tk.X, pady=(2, 10), ipady=4)

        q_lbl = tk.Label(card, text="", font=FONT_SMALL, fg=THEME_WARNING, bg=BG_CARD, wraplength=350, justify=tk.LEFT)
        q_lbl.pack(fill=tk.X, pady=(0, 10))

        tk.Label(card, text="Security Answer", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        ans_e = tk.Entry(card, font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        ans_e.pack(fill=tk.X, pady=(2, 10), ipady=4)

        tk.Label(card, text="New Password", font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_CARD, anchor="w").pack(fill=tk.X)
        new_pw_e = tk.Entry(card, show="*", font=FONT_BODY, bg=BG_CARD_LIGHT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief=tk.FLAT)
        new_pw_e.pack(fill=tk.X, pady=(2, 15), ipady=4)

        def verify_email_lookup():
            email = email_e.get().strip()
            ok, question = auth_service.get_security_question(email)
            if ok:
                q_lbl.config(text=f"Question: {question}")
            else:
                messagebox.showerror("Error", "No registered account found with this email.", parent=win)

        def execute_reset():
            email = email_e.get().strip()
            ans = ans_e.get().strip()
            new_pw = new_pw_e.get().strip()
            if not email or not ans or not new_pw:
                messagebox.showerror("Error", "Please fill in all fields.", parent=win)
                return
            if len(new_pw) < 6:
                messagebox.showerror("Error", "New password must be at least 6 characters.", parent=win)
                return
            ok, msg = auth_service.reset_password(email, ans, new_pw)
            if ok:
                messagebox.showinfo("Success", "Password reset successfully! You can now log in.", parent=win)
                win.destroy()
            else:
                messagebox.showerror("Error", msg, parent=win)

        lookup_btn = tk.Button(card, text="Verify Email & Fetch Question", font=FONT_SMALL, bg=THEME_PRIMARY, fg=TEXT_PRIMARY,
                               bd=0, cursor="hand2", command=verify_email_lookup)
        lookup_btn.pack(fill=tk.X, pady=(0, 10), ipady=3)

        reset_btn = tk.Button(card, text="Confirm Password Reset", font=FONT_BODY_BOLD, bg=THEME_SUCCESS, fg=TEXT_PRIMARY,
                              bd=0, cursor="hand2", command=execute_reset)
        reset_btn.pack(fill=tk.X, pady=(10, 0), ipady=6)
