import tkinter as tk
from tkinter import ttk, messagebox
from controllers.data import doctors, patients, appointments
from models.appointment import Appointment

class PatientView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F8FB")
        self.controller = controller
        label = tk.Label(
            self,
            text="Patient Dashboard",
            font=("Helvetica", 18, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        )
        label.pack(pady=15)
        
        btn_back = tk.Button(
            self,
            text="Back to menu",
            font=("Helvetica", 11, "bold"),
            bg="#6C757D",
            fg="white",
            activebackground="#5A6268",
            command=lambda: controller.show_frame("MainView")
        )
        btn_back.pack(pady=5)
        
        frame_login = tk.Frame(self, bg="#F4F8FB")
        frame_login.pack(pady=10)

        tk.Label(
            frame_login,
            text="Select Patient:",
            font=("Helvetica", 11, "bold"),
            bg="#F4F8FB"
        ).pack(side="left")

        self.patient_var = tk.StringVar(self)
        if patients:
            self.patient_var.set(patients[0].name)

        self.patient_dropdown = ttk.Combobox(
            frame_login,
            textvariable=self.patient_var,
            values=[p.name for p in patients],
            state="readonly",
            width=25
        )
        self.patient_dropdown.pack(side="left", padx=10)

        frame_booking = tk.LabelFrame(
            self,
            text="Book an Appointment",
            font=("Helvetica", 12, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88",
            padx=15,
            pady=15
        )
        frame_booking.pack(pady=10, fill="x", padx=20)

        # Doctor selection
        frame_d = tk.Frame(frame_booking, bg="#F4F8FB")
        frame_d.pack(pady=5, fill="x")

        tk.Label(frame_d, text="Select Doctor:", width=15, anchor="w", bg="#F4F8FB").pack(side="left")

        self.doctor_var = tk.StringVar(self)
        if doctors:
            self.doctor_var.set(doctors[0].name)

        self.doctor_dropdown = ttk.Combobox(
            frame_d,
            textvariable=self.doctor_var,
            values=[d.name for d in doctors],
            state="readonly"
        )
        self.doctor_dropdown.pack(side="left", fill="x", expand=True, padx=5)

        # Time slots
        frame_t = tk.Frame(frame_booking, bg="#F4F8FB")
        frame_t.pack(pady=5, fill="x")

        tk.Label(frame_t, text="Available Slots:", width=15, anchor="w", bg="#F4F8FB").pack(side="left")

        self.slots = ["09:00 AM", "10:00 AM", "11:30 AM", "01:00 PM", "02:30 PM", "04:00 PM"]
        self.time_var = tk.StringVar(self)
        self.time_var.set(self.slots[0])

        self.time_dropdown = ttk.Combobox(
            frame_t,
            textvariable=self.time_var,
            values=self.slots,
            state="readonly"
        )
        self.time_dropdown.pack(side="left", fill="x", expand=True, padx=5)

        # Book Button
        btn_book = tk.Button(
            frame_booking,
            text="Book Appointment",
            font=("Helvetica", 12, "bold"),
            bg="#2C7BE5",
            fg="white",
            activebackground="#1A5DC9",
            width=25,
            command=self.book_appointment
        )
        btn_book.pack(pady=15)

        # ================= APPOINTMENTS LIST =================
        tk.Label(
            self,
            text="All Scheduled Appointments:",
            font=("Helvetica", 12, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        ).pack(pady=5)

        list_frame = tk.Frame(self, bg="#F4F8FB")
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.appointments_listbox = tk.Listbox(
            list_frame,
            height=6,
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 11),
            bd=2,
            relief="groove"
        )
        self.appointments_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.appointments_listbox.yview)

    # ================= FUNCTIONS =================

    def update_view(self):
        self.appointments_listbox.delete(0, tk.END)
        for appt in appointments:
            text = f"🗓️ {appt.time_slot} | Dr. {appt.doctor.name} ({appt.doctor.specialty}) <=> Patient: {appt.patient.name}"
            self.appointments_listbox.insert(tk.END, text)

    def book_appointment(self):
        d_name = self.doctor_var.get()
        p_name = self.patient_var.get()
        time_slot = self.time_var.get()
        
        doctor = next((d for d in doctors if d.name == d_name), None)
        patient = next((p for p in patients if p.name == p_name), None)
        
        if doctor and patient and time_slot:
            for appt in appointments:
                if appt.doctor == doctor and appt.time_slot == time_slot:
                    messagebox.showerror("Conflict Error", f"Dr. {doctor.name} is already booked at {time_slot}.")
                    return
            
            new_appt = Appointment(doctor, patient, time_slot)
            appointments.append(new_appt)
            self.update_view()
            messagebox.showinfo("Appointment Confirmed", f"Appointment booked with Dr. {doctor.name} at {time_slot}.")