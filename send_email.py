import smtplib
import imghdr
from email.message import EmailMessage
import os

PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
SENDER = os.getenv("EMAIL")
RECEIVER = os.getenv("EMAIL")


def send_email(image):
    email_content = EmailMessage()
    email_content["Subject"] = "Object detected"
    email_content.set_content("A moving object was detected")

    with open(image, "rb") as file:
        content = file.read()

    email_content.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com")
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_content.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email("images/image_190.png")