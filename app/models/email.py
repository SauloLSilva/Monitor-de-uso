import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.models.mongodb import Mongodatabase
import subprocess

mongo = Mongodatabase()

class Email(object):
    def validar_email(self, email):
        # Regular expression pattern for basic email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return True
        else:
            return False

