import yagmail

from utilities.config_reader import get_config


def send_report_email(summary_html, zip_file_path):
    sender_email = get_config("Email","sender")
    app_password = get_config("Email","password")

    # Read recipients
    receivers_raw = get_config("Email", "receiver")
    cc_raw = get_config("Email", "cc")
    bcc_raw = get_config("Email", "bcc")

    receivers_mail = [email.strip() for email in receivers_raw.split(",") if email.strip()]
    cc_list = [email.strip() for email in cc_raw.split(",") if email.strip()]
    bcc_list = [email.strip() for email in bcc_raw.split(",") if email.strip()]

    subject = get_config("Email","subject")

    yag = yagmail.SMTP(user=sender_email, password=app_password)

    yag.send(
        to=receivers_mail,
        cc=cc_list or None,
        bcc=bcc_list or None,
        subject=subject,
        contents=summary_html,
        attachments=zip_file_path
    )

    # Logging
    print("\n📧 Email sent successfully!")
    print("TO:   ", ", ".join(receivers_mail))
    if cc_list:
        print("CC:   ", ", ".join(cc_list))
    if bcc_list:
        print("BCC:  ", ", ".join(bcc_list))
    print("FILE: ", zip_file_path)
