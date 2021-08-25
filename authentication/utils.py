from django.core.mail import send_mail



class Util:
    @staticmethod
    def send_email(data):
        # email = EmailMessage(subject=,body=data['email_body'])

        send_mail(data['email_subject'],data['email_body'],'email.sender852@gmail.com',[data['email']],fail_silently=False)