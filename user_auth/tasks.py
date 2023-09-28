import os

from django.core.mail import send_mail
from django.urls import reverse

from project.celery import app


@app.task
def send_email_with_celery(current_site, username, email, token):
    relative_link = reverse("user_auth:email-verify")
    abs_url = "http://" + current_site + relative_link + "?token=" + token
    email_body = (
        "Hi " + username + " Use the link below to verify your email \n" + abs_url
    )
    send_mail(
        subject="Verify your email",
        message=email_body,
        recipient_list=[email],
        from_email=os.getenv("EMAIL_HOST_USER"),
    )
