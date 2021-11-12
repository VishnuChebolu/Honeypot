import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import datetime
import pytz

load_dotenv()

password =  os.getenv('EMAIL_PASSWD')

def sendmail(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = f'Unauthorised activity detected on Honeypot'
    msg['From'] = "victim1729@gmail.com"
    msg['To'] = "victim1729@gmail.com"
    timenow = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d %B %Y %H:%M:%S")
    print(f'[{timenow}] : Drafting message.')
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("victim1729@gmail.com", password)
    s.send_message(msg)
    s.quit()
    timenow = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d %B %Y %H:%M:%S")
    print(f'[{timenow}] : Mail sent to admin.')
    return True


# sendmail("this is for testing in linux, dont worry")
