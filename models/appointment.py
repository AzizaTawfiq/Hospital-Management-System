class Appointment:
    def __init__(self, doctor, patient, time_slot, appt_id=None):
        self.appt_id = appt_id
        self.doctor = doctor
        self.patient = patient
        self.time_slot = time_slot
