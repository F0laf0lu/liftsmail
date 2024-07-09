from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'],
                        from_email = 'fromadmin@liftsmail.com.',
                        body=data['email_body'],
                        to=data['to_email'])
        email.send()        