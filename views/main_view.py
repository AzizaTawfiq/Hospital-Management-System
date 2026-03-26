import tkinter as tk

class MainView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F8FB")
        self.controller = controller
        
        title = tk.Label(self, text="Welcome to our hospital", font=("Helvetica", 18, "bold", "italic"))
        title.pack(pady=10)
        subtitle = tk.Label(self, text="Hoping you get well soon", font=("Helvetica", 14, "bold"))
        subtitle.pack(pady=10)
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20)
        btn_doctor = tk.Button(
            buttons_frame,
            text="Doctor View",
            font=("Helvetica", 14, "bold"),
            width=15,
            bg="#2C7BE5",
            fg="white",
            activebackground="#1A5DC9",
            activeforeground="white",
            command=lambda: controller.show_frame("DoctorView")
        )
        btn_doctor.pack(side="left", padx=10)
        
        btn_patient = tk.Button(
            buttons_frame,
            text="Patient View",
            font=("Helvetica", 14, "bold"),
            width=15,
            bg="#28A745",
            fg="white",
            activebackground="#1E7E34",
            activeforeground="white",
            command=lambda: controller.show_frame("PatientView")
        )
        btn_patient.pack(side="left", padx=10)
