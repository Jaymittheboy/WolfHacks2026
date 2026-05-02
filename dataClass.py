class personInfo:
    def __init__(self, OHIP, f_name, m_name, l_name, y_birth, m_birth, d_birth, gender, email, password):
        self.OHIP = OHIP
        self.f_name = f_name
        self.m_name = m_name
        self.l_name = l_name
        self.y_birth = y_birth
        self.m_birth = m_birth
        self.d_birth = d_birth
        self.gender = gender

        self.email = email

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

        