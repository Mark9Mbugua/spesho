from django.core.mail import EmailMultiAlternatives

# Sending email import
from .tokens import account_activation_token
from django.template.loader import render_to_string

# Token generating imports
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

# celery decorator import
from celery import shared_task

# decouple import
from decouple import config

@shared_task
def send_welcome_email(name, receiver, user):
    current_site = get_current_site(user)

    # Creating message subject and sender
    subject = 'Welcome to Dealie!!'
    sender = config('EMAIL_HOST_USER')

    # passing in the context variables
    text_content = render_to_string('activation.txt', {
        'name': name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_decode(urlsafe_base64_encode(force_bytes(user.pk))),
        'token': account_activation_token.make_token(user),
    })

    html_content = render_to_string('activation.html', {
        'name': name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_decode(urlsafe_base64_encode(force_bytes(user.pk))),
        'token': account_activation_token.make_token(user),
        })

    msg = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
