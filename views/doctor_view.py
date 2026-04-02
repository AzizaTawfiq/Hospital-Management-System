import tkinter as tk
from tkinter import ttk, messagebox
from controllers.db import get_all_patients

class DoctorView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F8FB")
        self.controller = controller
        
        self.label = tk.Label(
            self,
            text="Doctor Dashboard",
            font=("Helvetica", 18, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        )
        self.label.pack(pady=15)
      
        selection_frame = tk.Frame(self, bg="#F4F8FB")
        selection_frame.pack(pady=15)

        tk.Label(selection_frame, text="Select Patient:", bg="#F4F8FB", font=("Helvetica", 11, "bold")).grid(row=0, column=0, padx=10, pady=8)
        self.patient_var = tk.StringVar(self)
        self.patient_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.patient_var,
            state="readonly",
            width=25
        )
        self.patient_dropdown.grid(row=0, column=1, padx=10, pady=8)
        
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=5)
        btn_view_record = tk.Button(
            buttons_frame,
            text="View Patient Medical Record",
            font=("Helvetica", 12, "bold"),
            bg="#17A2B8",
            fg="white",
            activebackground="#138496",
            width=30,
            command=self.view_record,
        )
        btn_view_record.pack(side="left", pady=5, padx=10)

        btn_back = tk.Button(
            buttons_frame,
            text="Logout",
            font=("Helvetica", 11, "bold"),
            bg="#6C757D",
            fg="white",
            activebackground="#5A6268",
            command=self.logout
        )
        btn_back.pack(side="left", pady=5)
        
        tk.Label(
            self,
            text="Write Prescription / Notes:",
            font=("Helvetica", 13, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        ).pack(pady=5)
        
        self.text_prescription = tk.Text(
            self,
            height=8,
            width=65,
            font=("Helvetica", 11),
            bd=2,
            relief="groove",
            padx=15,
            pady=15,
        )
        self.text_prescription.pack(pady=5, padx=15)
        
        btn_prescribe = tk.Button(
            self,
            text="Add to Medical Record",
            font=("Helvetica", 13, "bold"),
            bg="#28A745",
            fg="white",
            activebackground="#1E7E34",
            width=28,
            command=self.add_prescription
        )
        btn_prescribe.pack(pady=15)

        self.patients_data = []

    def update_view(self):
        if self.controller.current_user:
            self.label.config(text=f"Doctor Dashboard - Welcome Dr. {self.controller.current_user['name']}")
        
        self.patients_data = get_all_patients()
        if self.patients_data:
            self.patient_dropdown['values'] = [p.name for p in self.patients_data]
            self.patient_dropdown.current(0)
        else:
            self.patient_dropdown['values'] = []
            self.patient_var.set("")

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginView")

    def view_record(self):
        p_name = self.patient_var.get()
        patient = next((p for p in self.patients_data if p.name == p_name), None)
        if patient:
            history = patient.medical_record.get_history()
            messagebox.showinfo(f"Medical history for {patient.name}", history)

    def add_prescription(self):
        p_name = self.patient_var.get()
        patient = next((p for p in self.patients_data if p.name == p_name), None)
        text = self.text_prescription.get("1.0", tk.END).strip()
        
        if not self.controller.current_user:
            return

        if patient and text:
            # We must import Doctor to use writePrescription, but Doctor object is needed
            # For simplicity let's just use the current_user's dict values to build a dummy Doctor
            from models.doctor import Doctor
            doctor = Doctor(self.controller.current_user["id"], self.controller.current_user["name"], self.controller.current_user["specialty"])
            
            doctor.writePrescription(patient, text)
            messagebox.showinfo("Success", "Prescription added successfully.")
            self.text_prescription.delete("1.0", tk.END)
            # Update the local object just so view_record works without DB refresh immediately
            self.patients_data = get_all_patients()
        else:
            messagebox.showwarning("Warning", "Please select a patient and write a prescription.")