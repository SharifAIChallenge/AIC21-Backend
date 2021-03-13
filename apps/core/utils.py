import json
import string
import random

from django.conf import settings
import telegram

LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation


def send_email(subject, template_name, context,
               from_email=settings.EMAIL_HOST_USER,
               receipts=None, file_path=None, file_name=None,
               file_content=None, mime_type=None):
    from django.core.mail.message import EmailMultiAlternatives
    from django.core.mail import DEFAULT_ATTACHMENT_MIME_TYPE
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags

    if receipts is None:
        receipts = []

    email_message_html = render_to_string(template_name, context=context)
    email_message_plaintext = strip_tags(email_message_html)

    email = EmailMultiAlternatives(
        subject=subject,
        body=email_message_plaintext,
        from_email=from_email,
        to=receipts
    )
    email.attach_alternative(email_message_html, 'text/html')
    if file_path:
        email.attach_file(file_path, mimetype=DEFAULT_ATTACHMENT_MIME_TYPE)
    if file_content:
        email.attach(filename=file_name, content=file_content,
                     mimetype=mime_type)
    email.send()


def send_to_telegram(dict):
    # todo set proxy after deploy
    # REQUEST_KWARGS = {
    #     # "USERNAME:PASSWORD@" is optional, if you need authentication:
    #     'proxy_url': 'http://127.0.0.1:12733/',
    # }
    bot = telegram.Bot(token='1603176620:AAEEjAyO6MUyYG1ycudQusoI3YkZulZW6rQ')
    bot.send_message("@ai_challange_alert", json.dumps(dict, indent=4))


def get_password_length():
    length = input("How long do you want your password: ")
    return int(length)


def password_generator(length=32):
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

    printable = list(printable)
    random.shuffle(printable)

    random_password = random.choices(printable, k=length)
    random_password = ''.join(random_password)
    return random_password
