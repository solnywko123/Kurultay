from django.core.mail import send_mail
from django.utils.html import format_html
from celery import shared_task


@shared_task()
def send_confirmation_email(email, code):
    activation_url = f'http://16.170.220.27/api/account/activate/?u={code}'

    message = format_html(
        '<h2>Hello, activate your account!</h2>\n'
        'Click on the word to activate'
        "<br><a href={}>{}</a></br>"
        "<p>Don't show it anyone</p>",
        activation_url,
        'CLICK HERE'
    )

    send_mail(
        'Hello, activate your account!',
        '',
        'checkemail@gmail.com',
        [email],
        fail_silently=False,
        html_message=message
    )

