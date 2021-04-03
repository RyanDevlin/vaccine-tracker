from requests_html import HTMLSession
import sys
import time


TURBO_VAX_URL = "https://www.turbovax.info/"

def check_availability():
    session = HTMLSession()
    r = session.get(TURBO_VAX_URL)
    r.html.render()
    pg = r.html.text
    availability = r.html.xpath('//*[@id="root"]/div/div[2]/div/div[3]/div[1]/div/div/div/div[2]/div/p')[0].full_text
    print(availability)

    if 'Not Available' in availability:
        return False
    
    return True


if __name__ == "__main__":
    while True:
        try:
            check_availability()
            time.sleep(5)
        except KeyboardInterrupt:
            sys.exit()