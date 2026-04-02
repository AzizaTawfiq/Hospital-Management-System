import tkinter as tk
from tkinter import messagebox
from controllers.db import login_user

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F8FB")
        self.controller = controller

        label = tk.Label(
            self,
            text="Login to Hospital System",
            font=("Helvetica", 18, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        )
        label.pack(pady=20)

        frame = tk.Frame(self, bg="#F4F8FB")
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Helvetica", 12), bg="#F4F8FB").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(frame, font=("Helvetica", 12), width=25)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame, text="Password:", font=("Helvetica", 12), bg="#F4F8FB").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(frame, font=("Helvetica", 12), show="*", width=25)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        btn_login = tk.Button(
            self,
            text="Login",
            font=("Helvetica", 12, "bold"),
            bg="#28A745",
            fg="white",
            activebackground="#1E7E34",
            width=20,
            command=self.handle_login
        )
        btn_login.pack(pady=15)

        btn_register = tk.Button(
            self,
            text="Create an Account",
            font=("Helvetica", 11, "bold"),
            bg="#2C7BE5",
            fg="white",
            activebackground="#1A5DC9",
            width=20,
            command=lambda: controller.show_frame("RegisterView")
        )
        btn_register.pack(pady=5)

    def update_view(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter username and password.")
            return

        success, data = login_user(username, password)
        if success:
            self.controller.current_user = data
            if data["role"] == "Doctor":
                self.controller.show_frame("DoctorView")
            elif data["role"] == "Patient":
                self.controller.show_frame("PatientView")
        else:
            messagebox.showerror("Login Failed", data)
