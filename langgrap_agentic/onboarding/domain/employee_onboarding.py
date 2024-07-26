from typing import List

class EmployeeOnboarding:
    def __init__(self, onboarding_id: str, name: str, email: str, phone: str, 
                 position: str, department: str, employee_documents: List[str] = None):
        self.onboarding_id = onboarding_id
        self.name = name
        self.email = email
        self.phone = phone
        self.position = position
        self.department = department
        self.employee_documents = employee_documents if employee_documents is not None else []
