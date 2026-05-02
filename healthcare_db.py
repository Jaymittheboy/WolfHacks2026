# =============================================================================
# Simplified Healthcare Database System
# Uses ONLY built-in Python — ZERO imports.
# =============================================================================

# =============================================================================
# SECTION 1 — ENCRYPTION & HASHING
# =============================================================================

SECRET_KEY = 42

def encrypt(text):
    result = ""
    for char in str(text):
        shifted = ord(char) + SECRET_KEY
        if shifted > 126: shifted -= 94
        result += chr(shifted)
    return result

def decrypt(text):
    result = ""
    for char in text:
        shifted = ord(char) - SECRET_KEY
        if shifted < 32: shifted += 94
        result += chr(shifted)
    return result

def hash_password(password):
    # A very basic custom hashing algorithm (for educational purposes)
    hash_val = 5381
    for char in password:
        hash_val = ((hash_val * 33) + ord(char)) % 4294967296
    return str(hash_val)

def check_password(entered_password, stored_hash):
    return hash_password(entered_password) == stored_hash


# =============================================================================
# SECTION 2 — VALIDATION
# =============================================================================

def validate_ohip(ohip):
    if len(ohip) != 10 or not ohip.isdigit():
        raise ValueError("OHIP must be exactly 10 digits.")
    return ohip

def validate_email(email):
    if "@" not in email or "." not in email:
        raise ValueError("Invalid email address.")
    return email

def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    has_upper = False
    has_lower = False
    has_digit = False
    for char in password:
        if char.isupper(): has_upper = True
        if char.islower(): has_lower = True
        if char.isdigit(): has_digit = True
    if not (has_upper and has_lower and has_digit):
        raise ValueError("Password must contain uppercase, lowercase, and a number.")


ROLE_PERMISSIONS = {
    "admin":     ["read", "write", "delete", "export", "view_audit"],
    "physician": ["read", "write", "export"],
    "nurse":     ["read", "write", "write_vitals"],
    "patient":   ["read_own"],
}


# =============================================================================
# SECTION 3 — AUDIT LOG
# =============================================================================

audit_log = []
audit_counter = 1 # Simple counter to track events

def log_event(action, who, what, record_id):
    global audit_counter

    audit_log.append({
        "event_id": audit_counter,
        "action": action,
        "who": who,
        "what": what,
        "record_id": record_id
    })

    audit_counter += 1


def check_permission(role, permission, who, record_id):
    if permission not in ROLE_PERMISSIONS.get(role, []):
        log_event("ACCESS DENIED", who, permission, record_id)
        raise PermissionError(f"'{role}' does not have '{permission}' permission.")


# =============================================================================
# SECTION 4 — PERSON INFO & PATIENT RECORD
# =============================================================================

class PatientRecord:
    def __init__(self, ohip, f_name, l_name, y_birth, gender, email, password):
        # Validate
        ohip = validate_ohip(ohip)
        email = validate_email(email)
        validate_password(password)

        # ID and basic calculation
        self.record_id = ohip[:4] + str(y_birth) + f_name[0] + l_name[0]
        self.is_deleted = False
        age = 2026 - y_birth # Basic calculation using current year

        # Encrypt and store data
        self._ohip = encrypt(ohip)
        self._f_name = encrypt(f_name)
        self._l_name = encrypt(l_name)
        self._gender = encrypt(gender.lower())
        self._age = encrypt(str(age))
        self._email = encrypt(email)
        self._password_hash = hash_password(password)
        
        # Clinical Data
        self.vitals = []
        self.conditions = []
        self.prescriptions = []

        log_event("CREATE", "system", "PatientRecord", self.record_id)

    # SECURE GETTERS
    def get_full_name(self, who, role):
        check_permission(role, "read", who, self.record_id)
        log_event("READ", who, "name", self.record_id)
        return decrypt(self._f_name) + " " + decrypt(self._l_name)

    def get_age(self, who, role):
        check_permission(role, "read", who, self.record_id)
        return int(decrypt(self._age))

    def check_login(self, entered_password):
        return check_password(entered_password, self._password_hash)

    # CLINICAL METHODS
    def add_vital(self, vital_name, value, who, role):
        check_permission(role, "write_vitals", who, self.record_id)
        reading = {"vital": vital_name, "value": value, "recorded_by": who}
        self.vitals.append(reading)
        log_event("UPDATE", who, f"vitals.{vital_name}", self.record_id)

    def add_condition(self, condition, severity, who, role):
        check_permission(role, "write", who, self.record_id)
        entry = {"condition": condition, "severity": severity, "added_by": who}
        self.conditions.append(entry)
        log_event("UPDATE", who, "conditions", self.record_id)


# =============================================================================
# SECTION 5 — DATA EXPORT & DATABASE
# =============================================================================

def export_patient(patient, who, role, anonymize=False):
    check_permission(role, "export", who, patient.record_id)
    
    data = {}
    
    if anonymize:
        age = patient.get_age(who, role)
        data["demographics"] = {
            "age_band": "Under 18" if age < 18 else "18 or older",
            "gender": decrypt(patient._gender),
        }

    else:
        data["demographics"] = {
            "ohip": decrypt(patient._ohip),
            "full_name": patient.get_full_name(who, role),
            "age": patient.get_age(who, role),
            "email": decrypt(patient._email),
        }

    data["vitals"] = patient.vitals
    data["conditions"] = patient.conditions

    log_event("EXPORT", who, "PatientRecord", patient.record_id)
    
    # Replaces 'json.dumps' with Python's basic string conversion for dicts
    return str(data)

class PatientDatabase:
    def __init__(self):
        self.records = {}

    def add(self, patient, who, role):
        check_permission(role, "write", who, patient.record_id)
        self.records[patient.record_id] = patient
        log_event("CREATE", who, "PatientDatabase", patient.record_id)

    def get(self, record_id, who, role):
        if record_id not in self.records:
            raise LookupError("Record not found.")
        patient = self.records[record_id]
        check_permission(role, "read", who, record_id)
        return patient


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("=== Simplified Healthcare Database ===\n")

    DOCTOR = "dr_smith"
    NURSE  = "nurse_jones"

    # 1. Create Patient
    patient = PatientRecord(
        ohip="1234567890",
        f_name="Jane", 
        l_name="Doe",
        y_birth=1985, 
        gender="female",
        email="jane.doe@email.com",
        password="SecurePass1"
    )
    print("Patient created. Record ID:", patient.record_id)
    print("Name:", patient.get_full_name(DOCTOR, "physician"))

    # 2. Add Medical Data
    patient.add_vital("heart_rate", "72 bpm", NURSE, "nurse")
    patient.add_condition("Type 2 Diabetes", "moderate", DOCTOR, "physician")

    # 3. Export Data (Dictionary String)
    print("\n--- Exported Data ---")
    output = export_patient(patient, DOCTOR, "physician", anonymize=False)
    print(output)

    # 4. View Audit Log
    print("\n--- Audit Log ---")
    for entry in audit_log:
        print(f"Event {entry['event_id']}: {entry['action']} by {entry['who']} on {entry['what']}")