from .person import Person
from .medical_record import MedicalRecord

class Patient(Person):
    def __init__(self, person_id, name):
        super().__init__(person_id, name)
        # Composition: Each patient has a medical record
        self.medical_record = MedicalRecord()
