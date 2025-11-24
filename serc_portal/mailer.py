import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class Mailer:
    def __init__(self, host, port, user, password, from_email):
        self.host = host; self.port = port
        self.user = user; self.password = password
        self.from_email = from_email
    def send(self, to_email, subject, body):
        if not self.host: return False
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = formataddr(('CSIR-SERC', self.from_email))
        msg['To'] = to_email
        with smtplib.SMTP(self.host, self.port) as s:
            s.starttls()
            if self.user:
                s.login(self.user, self.password)
            s.sendmail(self.from_email, [to_email], msg.as_string())
        return True
