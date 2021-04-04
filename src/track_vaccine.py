from requests_html import HTMLSession
import time
import os

from src.state_manager import StateManager

TURBO_VAX_URL = "https://www.turbovax.info/"

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



if __name__ == "__main__":
    poll_availability()