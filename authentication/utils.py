from django.conf import settings
from django.core.mail import send_mail

def send_email_token(email,token):
    try:
      
        subject = 'Your account need to verfied'
        message = f'Click on the link to verify http://127.0.0.1:8000/authentication/account/{token}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )
    except Exception as e:
        print(f'send email Error ${e}')
        return False
    return True