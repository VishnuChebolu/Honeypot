import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib

load_dotenv()

password =  os.getenv('EMAIL_PASSWD')

def sendmail(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = f'Unauthorised activity detected on Honeypot'
    msg['From'] = "victim1729@gmail.com"
    msg['To'] = "victim1729@gmail.com"
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("victim1729@gmail.com", password)
    s.send_message(msg)
    s.quit()
    print("message sent")
    return True

