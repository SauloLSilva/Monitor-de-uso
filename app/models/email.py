import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email(object):
    def validar_email(self, email):
        # Regular expression pattern for basic email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return True
        else:
            return False
        
    def connect(self):
        try:
            # Configurações do servidor SMTP
            smtp_host = 'smtp.office365.com'
            smtp_port = 587
            smtp_user = 'monitor_uso@outlook.com'
            smtp_password = ''
            return (smtp_host, smtp_password, smtp_user, smtp_port)
        except Exception as err:
            print(err)

    def sender(self, dado):
        try:
            # Informações do e-mail
            sender = 'monitor_uso@outlook.com'
            receiver = ''
            subject = 'Relatório de uso'
            body = f'Prezado,\n\nSegue Relatório de uso:\n\n{dado}'

            # Criação do objeto MIMEMultipart
            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = receiver
            message['Subject'] = subject

            # Adiciona o corpo do e-mail
            message.attach(MIMEText(body, 'plain'))

            # Conexão com o servidor SMTP
            server = smtplib.SMTP(self.connect()[0], self.connect()[3])
            server.starttls()
            server.login(self.connect()[2], self.connect()[1])

            # Envio do e-mail
            server.sendmail(sender, receiver, message.as_string())

            # Encerra a conexão com o servidor SMTP
            server.quit()
        except Exception as err:
            print(err)
