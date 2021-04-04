from requests_html import HTMLSession
import sys
import time
import smtplib
import base64
import json

TURBO_VAX_URL = "https://www.turbovax.info/"
#"tkobil17@gmail.com"

sender = 'nycvaccinebot@gmail.com'
#receivers = ['rdevlin.mail@gmail.com']

def check_availability():
    session = HTMLSession()
    r = session.get(TURBO_VAX_URL)
    r.html.render()
    pg = r.html.text
    availability = r.html.xpath('//*[@id="root"]/div/div[2]/div/div[3]/div[1]/div/div/div/div[2]/div/p')[0].full_text
    print(pg)

    #send_email()

    if 'Not Available' in availability:
        return False
    
    return True

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

     check_availability()
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