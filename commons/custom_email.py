import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import EMAIL_HOST_USER
from settings import EMAIL_HOST_PASSWORD

sender_address = EMAIL_HOST_USER
sender_pass = EMAIL_HOST_PASSWORD
receiver_address = 'pransh.mail@gmail.com'


def send_help_request_email(user_name, is_guest_user, user_email, message):
    message = 'User: '+user_name+'\nEmail: '+user_email+'\nReported a issue in superteacher. \nIssue is: '+message+'\n'
    if is_guest_user:
        message += 'The user is a guest user'

    subject = 'User Reported an Issue in Superteacher'

    send_email_common(message=message, subject=subject)


def send_question_bug_report_email(user_email, question_id, bug_title, bug_description):
    message = 'User: ' + user_email + '\nReported bug in question: ' + str(question_id) + '\nBug Title is: ' \
              + bug_title + '\nBug Description is: ' + bug_description

    subject = 'Bug in Question reported by student!'

    send_email_common(message=message, subject=subject)


def send_email_common(message, subject):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=['Studykitco@gmail.com', 'info@superteacher.pk'],
        fail_silently=False,
    )
