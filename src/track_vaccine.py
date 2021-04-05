import hashlib
import json
import os
import sys
import time

import geckodriver_autoinstaller
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from src.email_alert import email
from src.state_manager import StateManager

TURBO_VAX_URL = "https://www.turbovax.info/"

class VaccinationSite(object):
    def __init__(self, name, neighborhood, numAvailable, time):
        self.name = name
        self.neighborhood = neighborhood
        self.time = time # Formatted like Apr 8 - 1:15PM
        self.numAvailable = numAvailable

    def __str__(self):
        return("{} in {} currently has appointment(s) available".format(self.name,self.neighborhood))
    
    def __eq__(self, other):
        return self.name == other.name

def determineState(sites):
    with open("config.json",'r') as fh:
        data = json.loads(fh)
        subject = "New Vaccine Appointments!"
        body = "<p><b>Vaccination Sites Availabile:</b><br>Schedule on <a href=\"" + data['endpoint']['link'] + "\">" + data['endpoint']['name'] + "</a><br><br>"
       
        for site in sites:
            body += str(site) + "<br><br>"
        body + "</p>"
        StateManager.set_state(sites,lambda: email(data['username'], data['password'], data['receivers'], subject, body))

def poll_availability():
    # create webdriver object
    options = Options()
    options.headless = True
    geckodriver_autoinstaller.install() 
    driver = webdriver.Firefox(options=options)

    while True:
        try:
            # get google.co.in
            driver.get(TURBO_VAX_URL)
            time.sleep(0.2) # Need a fraction of a second for the page to execute js 
            result = driver.find_element_by_css_selector('div.MuiBox-root.jss14')
            status = result.text.replace('(', '').replace(')', '')
            print(status.split(" "))

            # If not not available, continue loop
            if status.split(" ")[1] == "Not":
                time.sleep(5)
                continue

            results = driver.find_elements_by_css_selector('div.MuiCardContent-root.jss39')
            sites = []
            # Build object for each location with availability
            for item in results:
                data = item.text.splitlines()
                
                site = VaccinationSite(data[0].strip().replace('–', '-'), data[1].strip().replace('–', '-'), data[2].split("·")[1].strip().split(" ")[0].replace('–', '-'), data[3].strip().replace('–', '-'))
                sites.append(site)
            
            determineState(sites)
            time.sleep(5)
        except KeyboardInterrupt:
            driver.quit()
            sys.exit()
if __name__ == "__main__":
        poll_availability()