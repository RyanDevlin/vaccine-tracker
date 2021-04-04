from requests_html import HTMLSession
import time
import smtplib
import base64
import json
import os

from src.state_manager import StateManager

TURBO_VAX_URL = "https://www.turbovax.info/"
#"tkobil17@gmail.com"

sender = 'nycvaccinebot@gmail.com'
#receivers = ['rdevlin.mail@gmail.com']

def poll_availability():
    while True:
        try:
            session = HTMLSession()
            response = session.get(TURBO_VAX_URL)
            wait = response.html.render()
            pg = response.html.text
            availability = response.html.xpath('//*[@id="root"]/div/div[2]/div/div[3]/div[1]/div/div/div/div[2]/div/p')[0].full_text
            print(availability)
            # TODO - StateManager.set_state(state) (state = 'Available' or 'Not Available')
            session.close()
            time.sleep(15)

        except KeyboardInterrupt:
            session.close()
            sys.exit()


def send_email(account, password, receivers, subject, body):
    # Assumes password is base64 encoded
    decode_pass = base64.b64decode(password).decode("utf-8")
    print(decode_pass)

    FROM = account
    TO = receivers
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(account, decode_pass)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print("failed to send mail")
        print(e)


if __name__ == "__main__":
    with open("config.json",'r') as fh:
     data = fh.read()
     data = json.loads(data)
     subject = "New Vaccine Appointments!"
     body = "New appointments for the covid vaccine are available at CVS! Schedule them here: <link_to_cvs_website>"
     #send_email(data['username'], data['password'], data['receivers'], subject, body)

     poll_availability()
"""
    while True:
        try:
            #result = check_availability()
            #print(result)
            send_email()
            time.sleep(5)
        except KeyboardInterrupt:
            sys.exit()
"""
