import tkinter as tk
from tkinter import ttk, messagebox
from controllers.db import get_all_doctors, get_appointments, add_appointment

class PatientView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F8FB")
        self.controller = controller
        self.label = tk.Label(
            self,
            text="Patient Dashboard",
            font=("Helvetica", 18, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        )
        self.label.pack(pady=15)
        
        btn_back = tk.Button(
            self,
            text="Logout",
            font=("Helvetica", 11, "bold"),
            bg="#6C757D",
            fg="white",
            activebackground="#5A6268",
            command=self.logout
        )
        btn_back.pack(pady=5)
        
        frame_booking = tk.LabelFrame(
            self,
            text="Book an Appointment",
            font=("Helvetica", 12, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88",
            padx=15,
            pady=5
        )
        frame_booking.pack(pady=10, fill="x", padx=20)

        # Doctor selection
        frame_d = tk.Frame(frame_booking, bg="#F4F8FB")
        frame_d.pack(pady=5, fill="x")

        tk.Label(frame_d, text="Select Doctor:", width=15, anchor="w", bg="#F4F8FB").pack(side="left")

        self.doctor_var = tk.StringVar(self)
        self.doctor_dropdown = ttk.Combobox(
            frame_d,
            textvariable=self.doctor_var,
            state="readonly"
        )
        self.doctor_dropdown.pack(side="left", fill="x", expand=True, padx=5)

        # Time slots
        frame_t = tk.Frame(frame_booking, bg="#F4F8FB")
        frame_t.pack(pady=5, fill="x")

        tk.Label(frame_t, text="Available Slots:", width=15, anchor="w", bg="#F4F8FB").pack(side="left")

        self.slots = ["09:00 AM", "10:00 AM", "11:30 AM", "01:00 PM", "02:30 PM", "04:00 PM"]
        self.time_var = tk.StringVar(self)
        
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

        tk.Label(
            self,
            text="My Scheduled Appointments:",
            font=("Helvetica", 12, "bold"),
            bg="#F4F8FB",
            fg="#1F3C88"
        ).pack(pady=5)

        list_frame = tk.Frame(self, bg="white", bd=2, relief="groove")
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0, height=120)
        self.scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.doctors_data = []

    def update_view(self):
        if not self.controller.current_user:
            return
            
        self.label.config(text=f"Patient Dashboard - Welcome {self.controller.current_user['name']}")
        
        self.doctors_data = get_all_doctors()
        if self.doctors_data:
            self.doctor_dropdown['values'] = [f"{d.name} ({d.specialty})" for d in self.doctors_data]
            self.doctor_dropdown.current(0)
            self.time_dropdown.current(0)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        from controllers.db import get_appointments
        all_appts = get_appointments()
        for appt in all_appts:
            if appt.patient.person_id == self.controller.current_user["id"]:
                row_frame = tk.Frame(self.inner_frame, bg="white")
                row_frame.pack(fill="x", pady=2, padx=5)
                
                text = f"🗓️ {appt.time_slot} | Dr. {appt.doctor.name} ({appt.doctor.specialty})"
                lbl = tk.Label(row_frame, text=text, font=("Helvetica", 11), bg="white")
                lbl.pack(side="left")
                
                btn_remove = tk.Button(
                    row_frame,
                    text="❌",
                    fg="red",
                    bg="white",
                    bd=0,
                    cursor="hand2",
                    font=("Helvetica", 10, "bold"),
                    command=lambda a_id=appt.appt_id: self.delete_appointment(a_id)
                )
                btn_remove.pack(side="right", padx=5)

    def delete_appointment(self, appt_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this appointment?"):
            from controllers.db import remove_appointment
            remove_appointment(appt_id)
            self.refresh_list()

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginView")

    def book_appointment(self):
        d_index = self.doctor_dropdown.current()
        time_slot = self.time_var.get()
        
        if d_index == -1 or not time_slot:
            messagebox.showwarning("Warning", "Select doctor and time.")
            return

        doctor = self.doctors_data[d_index]
        patient_id = self.controller.current_user["id"]
        
        all_appts = get_appointments()
        for appt in all_appts:
            if appt.doctor.person_id == doctor.person_id and appt.time_slot == time_slot:
                messagebox.showerror("Conflict Error", f"Dr. {doctor.name} is already booked at {time_slot}.")
                return
        
        add_appointment(doctor.person_id, patient_id, time_slot)
        self.refresh_list()
        messagebox.showinfo("Appointment Confirmed", f"Appointment booked with Dr. {doctor.name} at {time_slot}.")