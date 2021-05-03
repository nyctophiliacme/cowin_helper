import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import EMAIL_HOST_USER
from settings import EMAIL_HOST_PASSWORD
from settings import EMAIL_HOST
from settings import EMAIL_PORT

sender_address = EMAIL_HOST_USER
sender_pass = EMAIL_HOST_PASSWORD
receiver_address = 'pransh.mail@gmail.com'


def send_email():
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'

    mail_content = '''Hello,
    This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
    Thank You
    '''

    message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
