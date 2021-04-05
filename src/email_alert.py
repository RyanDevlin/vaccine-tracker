import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.message as message

def email(account, password, receivers, subject, body):
    # Assumes password is base64 encoded
    decode_pass = base64.b64decode(password).decode("utf-8")

    msg = message.EmailMessage()
    msg['Subject'] = subject
    msg['From'] = account
    msg['To'] = receivers
    msg.add_header('Content-Type','text/html')
    msg.set_payload(body)

    # Prepare actual message
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(account, decode_pass)
        server.sendmail(msg['From'], receivers.split(','), msg.as_string())
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        import traceback
        traceback.format_exc()

