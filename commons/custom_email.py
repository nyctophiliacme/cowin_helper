import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import EMAIL_HOST_USER
from settings import EMAIL_HOST_PASSWORD
from settings import EMAIL_HOST
from settings import EMAIL_PORT


def send_email_helper(receiver_address, message_body):
    sender_address = EMAIL_HOST_USER
    sender_pass = EMAIL_HOST_PASSWORD
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Good news! Covid-19 vaccines are available in your locality'

    mail_content = message_body

    message.attach(MIMEText(mail_content, 'plain'))
    send_email_common(message, sender_address, sender_pass, receiver_address)


def send_email_common(message, sender_address, sender_pass, receiver_address):
    session = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
