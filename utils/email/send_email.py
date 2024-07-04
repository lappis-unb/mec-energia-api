import smtplib
from email.message import Message

from mec_energia import settings

from .templates_email import password_templates_email
from .valid_email import verify_email_is_valid

MEC_ENERGIA_EMAIL = settings.MEC_ENERGIA_EMAIL
MEC_ENERGIA_EMAIL_APP_PASSWORD = settings.MEC_ENERGIA_EMAIL_APP_PASSWORD

def send_email_first_access_password(user_name, university_name, recipient_email, link_to_reset_password_page):
    title, text_body = password_templates_email.template_email_first_access(user_name, university_name, link_to_reset_password_page)

    verify_email_is_valid(recipient_email)

    send_email(MEC_ENERGIA_EMAIL, MEC_ENERGIA_EMAIL_APP_PASSWORD, recipient_email, title, text_body)

def send_email_reset_password(user_name, recipient_email, link_to_reset_password_page):
    title, text_body = password_templates_email.template_email_recovery_password(user_name, link_to_reset_password_page)

    verify_email_is_valid(recipient_email)

    send_email(MEC_ENERGIA_EMAIL, MEC_ENERGIA_EMAIL_APP_PASSWORD, recipient_email, title, text_body)

def send_email_reset_password_by_admin(user_name, recipient_email, link_to_reset_password_page):
    title, text_body = password_templates_email.template_email_recovery_password_by_admin(user_name, link_to_reset_password_page)

    verify_email_is_valid(recipient_email)

    send_email(MEC_ENERGIA_EMAIL, MEC_ENERGIA_EMAIL_APP_PASSWORD, recipient_email, title, text_body)

def send_email(sender_email: str, sender_password: str, recipient_email: str, title: str, text_body: str):
    try:
        msg = Message()
        msg['Subject'] = title
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(text_body)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        
        s.login(msg['From'], sender_password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    except Exception as error:
        raise Exception(f'Error Send Email: {str(error)}')
