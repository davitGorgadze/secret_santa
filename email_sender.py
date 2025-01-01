import os
import smtplib
import ssl
from typing import Set

from tqdm import tqdm
from file_reader import Santa
from pair_generator import SantaRecipientPair
from email.message import EmailMessage

app_password = os.getenv("EMAIL_APP_PASSWORD")
if not app_password:
    raise ValueError("The EMAIL_APP_PASSWORD environment variable is not set.")

email_sender = os.getenv("MY_EMAIL_ADDRESS")


class EmailSender:

    def __init__(self, pairs: Set[SantaRecipientPair], template_file_path: str):
        self.pairs: Set[SantaRecipientPair] = pairs
        self.template_file_path = template_file_path

    def load_template(self) -> str:
        with open(self.template_file_path, 'r', encoding='utf-8-sig') as template_file:
            return template_file.read()

    def send_email(self, pair: SantaRecipientPair):
        template = self.load_template()

        subject, body = template.split('\n', 1)

        sender_name = pair.sender.name.split(" ")[0]
        body = body.format(sender_name=sender_name, recipient_name=pair.receiver.name)
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = pair.sender.email
        em["Subject"] = subject
        em.set_content(body, subtype="plain", charset='utf-8')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
            smtp.login(email_sender, app_password)
            smtp.sendmail(email_sender, pair.sender.email, em.as_string())

    def send_all_emails(self):
        for pair in tqdm(self.pairs, desc="Sending Emails ...."):
            self.send_email(pair)
        print("All Emails Have Been Sent!")