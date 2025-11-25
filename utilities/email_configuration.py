import yagmail
from utilities.config_reader import get_config


def send_report_email(html_body):
    sender = get_config("Email", "sender")
    pwd = get_config("Email", "password")

    receivers = [
        email.strip() for email in get_config("Email", "receiver").split(",")
        if email.strip()
    ]

    subject = get_config("Email", "subject")

    yag = yagmail.SMTP(user=sender, password=pwd)

    contents = [html_body]

    yag.send(
        to=receivers,
        subject=subject,
        contents=contents
    )
