import os

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class Supporting:
    @staticmethod
    def send_email(request, user):
        current_site = get_current_site(request).domain
        relative_link = reverse("user_auth:email-verify")
        token = RefreshToken.for_user(user)
        abs_url = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
            "Hi "
            + user.username
            + " Use the link below to verify your email \n"
            + abs_url
        )
        send_mail(
            subject="Verify your email",
            message=email_body,
            recipient_list=[user.email],
            from_email=os.getenv("EMAIL_HOST_USER"),
        )
