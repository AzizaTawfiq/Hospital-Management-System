import tkinter as tk
from tkinter import messagebox
from controllers.db import register_user

class RegisterView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F8FB")
        self.controller = controller

        label = tk.Label(
            self,
            text="Register Account",
            font=("Helvetica", 18, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        )
        label.pack(pady=10)

        frame = tk.Frame(self, bg="#F4F8FB")
        frame.pack(pady=5)

        tk.Label(frame, text="Username:", font=("Helvetica", 11), bg="#F4F8FB").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(frame, font=("Helvetica", 11), width=25)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Password:", font=("Helvetica", 11), bg="#F4F8FB").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(frame, font=("Helvetica", 11), show="*", width=25)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Full Name:", font=("Helvetica", 11), bg="#F4F8FB").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(frame, font=("Helvetica", 11), width=25)
        self.name_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame, text="Role:", font=("Helvetica", 11), bg="#F4F8FB").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        
        self.role_var = tk.StringVar(value="Patient")
        roles_frame = tk.Frame(frame, bg="#F4F8FB")
        roles_frame.grid(row=3, column=1, sticky="w")
        tk.Radiobutton(roles_frame, text="Patient", variable=self.role_var, value="Patient", bg="#F4F8FB", command=self.toggle_specialty).pack(side="left")
        tk.Radiobutton(roles_frame, text="Doctor", variable=self.role_var, value="Doctor", bg="#F4F8FB", command=self.toggle_specialty).pack(side="left")

        self.specialty_label = tk.Label(frame, text="Specialty:", font=("Helvetica", 11), bg="#F4F8FB")
        self.specialty_entry = tk.Entry(frame, font=("Helvetica", 11), width=25)

        btn_register = tk.Button(
            self,
            text="Register",
            font=("Helvetica", 12, "bold"),
            bg="#28A745",
            fg="white",
            activebackground="#1E7E34",
            width=20,
            command=self.handle_register
        )
        btn_register.pack(pady=15)

        btn_back = tk.Button(
            self,
            text="Back to Login",
            font=("Helvetica", 11, "bold"),
            bg="#6C757D",
            fg="white",
            activebackground="#5A6268",
            width=20,
            command=lambda: controller.show_frame("LoginView")
        )
        btn_back.pack(pady=5)
        self.toggle_specialty()

    def update_view(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.specialty_entry.delete(0, tk.END)
        self.role_var.set("Patient")
        self.toggle_specialty()

    def toggle_specialty(self):
        if self.role_var.get() == "Doctor":
            self.specialty_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
            self.specialty_entry.grid(row=4, column=1, padx=10, pady=5)
        else:
            self.specialty_label.grid_remove()
            self.specialty_entry.grid_remove()

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        name = self.name_entry.get().strip()
        role = self.role_var.get()
        specialty = self.specialty_entry.get().strip()

        if not username or not password or not name:
            messagebox.showwarning("Warning", "Please fill all required fields.")
            return

        if role == "Doctor" and not specialty:
            messagebox.showwarning("Warning", "Please enter a specialty for Doctor.")
            return

        success, msg = register_user(username, password, role, name, specialty)
        if success:
            messagebox.showinfo("Success", "Account created! You can now log in.")
            self.controller.show_frame("LoginView")
        else:
            messagebox.showerror("Error", msg)
