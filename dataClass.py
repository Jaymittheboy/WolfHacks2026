SECRET_KEY = 42  # Change this number to make your encryption unique

def encrypt(text):
    result = ""
    for char in str(text):
        shifted = ord(char) + SECRET_KEY
        if shifted > 126:
            shifted -= 94
        result += chr(shifted)
    return result

def decrypt(text):
    result = ""
    for char in text:
        shifted = ord(char) - SECRET_KEY
        if shifted < 32:
            shifted += 94
        result += chr(shifted)
    return result


class personInfo:
    def __init__(self, OHIP, f_name, m_name, l_name, y_birth, m_birth, d_birth, gender, email, password):
        self.OHIP = self.encrypt(OHIP)
        self.f_name = self.encrypt(f_name)
        self.m_name = self.encrypt(m_name)
        self.l_name = self.encrypt(l_name)
        self.y_birth = self.encrypt(str(y_birth))
        self.m_birth = self.encrypt(str(m_birth))
        self.d_birth = self.encrypt(str(d_birth))
        self.gender = self.encrypt(str(gender))
        self.age = self.encrypt(str(2026 - y_birth))

        self.email = self.encrypt(email)
        self.password = self.encrypt(password)

        self.phone = self.encrypt(phone)
        self.address = self.encrypt(address)
        self.emergency_contact = self.encrypt(emergency_contact)
        self.insurance_provider = self.encrypt(insurance_id)
        self.primary_physician = self.encrypt(physician_name)

class dataClass(personInfo):
    def __init__(self, ID, f_name, m_name, l_name, y_birth, m_birth, d_birth):
        super().__init__(ID, f_name, m_name, l_name, y_birth, m_birth, d_birth)
        self.medical_history = {"Conditions" : [],
                                "Surgeries" : [],
                                "Illnesses" : []}
        
        self.allergies = {"Food" : [],
                          "Medication" : [],
                          "Environmental" : []}

        self.test_results = {"Blood Pressure" : [],}

        self.risk_factors = {}

        self.prescriptions = {"Medication" : [],}

        self.disease_diagnosis = {}