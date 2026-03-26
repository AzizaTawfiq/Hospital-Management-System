from .person import Person

class Doctor(Person):
    def __init__(self, person_id, name, specialty):
        super().__init__(person_id, name)
        self.specialty = specialty
        
    def writePrescription(self, patient, prescription_text):
        patient.medical_record.add_record(f"Prescription by Dr. {self.name}: {prescription_text}")
