import re

class Check_email:
    def validar_email(self, email):
        # Regular expression pattern for basic email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return True
        else:
            return False