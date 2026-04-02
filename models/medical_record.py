from datetime import datetime

class MedicalRecord:
    def __init__(self, patient_id=None):
        # Private attribute to secure medical history
        self.__history = []
        self.patient_id = patient_id

    def add_record(self, record):
        from controllers.db import add_medical_record
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        formatted = f"[{timestamp}] {record}"
        self.__history.append(formatted)
        if self.patient_id is not None:
            add_medical_record(self.patient_id, formatted)

    def set_history(self, history):
        self.__history = history

    def get_history(self):
        if not self.__history:
            return "No medical history available."
        return "\n".join(self.__history)
