from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_mail(user, token):
    subject = "Welcome to DataSkipper"
    html_message = render_to_string(
        "user/activation_mail.html",  # Path to your HTML template
        {
            "user": user,
            "activation_link": f"{settings.SITE_URL}/iot-backend/api/v1/accountVerify/{token}/",
        },
    )
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(
        subject, plain_message, email_from, recipient_list, html_message=html_message
    )
