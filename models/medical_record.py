from datetime import datetime

class MedicalRecord:
    def __init__(self):
        # Private attribute to secure medical history
        self.__history = []

    def add_record(self, record):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.__history.append(f"[{timestamp}] {record}")

    def get_history(self):
        if not self.__history:
            return "No medical history available."
        return "\n".join(self.__history)
