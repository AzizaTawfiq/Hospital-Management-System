import tkinter as tk
from tkinter import ttk, messagebox
from controllers.data import doctors, patients

class DoctorView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F8FB")
        self.controller = controller
        label = tk.Label(
            self,
            text="Doctor Dashboard",
            font=("Helvetica", 18, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        )
        label.pack(pady=15)
      
        selection_frame = tk.Frame(self, bg="#F4F8FB")
        selection_frame.pack(pady=15)

        tk.Label(selection_frame, text="Select Doctor:", bg="#F4F8FB", font=("Helvetica", 11, "bold")).grid(row=0, column=0, padx=10, pady=8)
        self.doctor_var = tk.StringVar(self)
        if doctors:
            self.doctor_var.set(doctors[0].name)
        self.doctor_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.doctor_var,
            values=[d.name for d in doctors],
            state="readonly",
            width=25
        )
        self.doctor_dropdown.grid(row=0, column=1, padx=10, pady=8)
        
        tk.Label(selection_frame, text="Select Patient:", bg="#F4F8FB", font=("Helvetica", 11, "bold")).grid(row=1, column=0, padx=10, pady=8)
        self.patient_var = tk.StringVar(self)
        if patients:
            self.patient_var.set(patients[0].name)
        self.patient_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.patient_var,
            values=[p.name for p in patients],
            state="readonly",
            width=25
        )
        self.patient_dropdown.grid(row=1, column=1, padx=10, pady=8)
        
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20)
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
        btn_view_record.pack(side="left", pady=15, padx=10)

        btn_back = tk.Button(
            buttons_frame,
            text="Back to menu",
            font=("Helvetica", 11, "bold"),
            bg="#6C757D",
            fg="white",
            activebackground="#5A6268",
            command=lambda: controller.show_frame("MainView")
        )
        btn_back.pack(side="left", pady=15)
        
       
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

    # ================= FUNCTIONS =================

    def view_record(self):
        p_name = self.patient_var.get()
        patient = next((p for p in patients if p.name == p_name), None)
        if patient:
            history = patient.medical_record.get_history()
            messagebox.showinfo(f"Medical history for {patient.name}", history)

    def add_prescription(self):
        d_name = self.doctor_var.get()
        p_name = self.patient_var.get()
        
        doctor = next((d for d in doctors if d.name == d_name), None)
        patient = next((p for p in patients if p.name == p_name), None)
        text = self.text_prescription.get("1.0", tk.END).strip()
        
        if doctor and patient and text:
            doctor.writePrescription(patient, text)
            messagebox.showinfo("Success", "Prescription added successfully.")
            self.text_prescription.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Warning", "Please write a prescription before submitting.")