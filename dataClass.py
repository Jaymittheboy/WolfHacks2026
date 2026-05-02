class personInfo:
    def encrypt(self, text):
        encrypted_text = ""

        for char in text:
            encrypted_char = (ord(char) + 26)
            
            if encrypted_char > 126:
                encrypted_char -= 94

            encrypted_text += chr(encrypted_char)
        
        return encrypted_text
    
    def decrypt(self, encrypted_text):
        decrypted_text = ""

        for char in encrypted_text:
            decrypted_char = (ord(char) - 26)
            
            if decrypted_char < 32:
                decrypted_char += 94

            decrypted_text += chr(decrypted_char)
        
        return decrypted_text

    
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