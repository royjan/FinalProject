import sys
sys.path.append('FinalProject')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

from FinalProject.src.Log.Logger import Logger, TaskType

EMAIL_ADDRESS = "roy.afeka.project@gmail.com"
PASSWORD = "!Bj11235813"


def send_mail(to_addr: list, body, subject, file_name=None, delete_after_send=True):
    """
    :param to_addr: multiple emails
    :param body: content of the message
    :param subject: title of the mail
    :param file_name: if we want to attach file
    :param delete_after_send: do we want to delete file after mail sent
    """
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = ','.join(to_addr)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    if file_name:
        attach_file = open(file_name, 'rb')
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(attach_file.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_name))
        message.attach(payload)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(EMAIL_ADDRESS, PASSWORD)
    text = message.as_string()
    session.sendmail(PASSWORD, to_addr, text)
    session.quit()
    if delete_after_send and file_name:
        os.remove(os.path.basename(file_name))
    Logger.print("Mail sent!", task_type=TaskType.AGENT)
