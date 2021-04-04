import hashlib
import json
import os
import sys
import time

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
    def availability(self):
        print("{} in {} currently has appointment(s) available".format(self.name,self.neighborhood))
        return("{} in {} currently has appointment(s) available".format(self.name,self.neighborhood))

def determineState(sites):
    with open("config.json",'r') as fh:
        data = fh.read()
        data = json.loads(data)
        subject = "New Vaccine Appointments!"
        aggregateHash = ""
        body = "<p><b>Vaccination Sites Availabile:</b><br>Schedule on <a href=\"" + data['endpoint']['link'] + "\">" + data['endpoint']['name'] + "</a><br><br>"
        for site in sites:
            line = site.availability()
            body += line + "<br><br>"
            hashVal = hashlib.sha1(repr(line).encode('utf-8'))
            aggregateHash += hashVal.hexdigest()
        body + "</p>"
        result = hashlib.sha1(repr(aggregateHash).encode('utf-8'))
        state = result.hexdigest()

        #send_email(data['username'], data['password'], data['receivers'], subject, body)
        StateManager.set_state(state,lambda: email(data['username'], data['password'], data['receivers'], subject, body))
    print("STATE: ", StateManager.State)

class VaccinationSite(object):
    empCount = 0
    def __init__(self, name, neighborhood, numAvailable, time):
        self.name = name
        self.neighborhood = neighborhood
        self.time = time # Formatted like Apr 8 - 1:15PM
        self.numAvailable = numAvailable
    def availability(self):
        return("{} in {} currently has {} appointment(s) available at {}".format(self.name,self.neighborhood,self.numAvailable, self.time))

def determineState(sites):
    with open("config.json",'r') as fh:
        data = fh.read()
        data = json.loads(data)
        subject = "New Vaccine Appointments!"
        aggregateHash = ""
        body = "<p><b>Vaccination Sites Availabile:</b><br>Schedule on <a href=\"" + data['endpoint']['link'] + "\">" + data['endpoint']['name'] + "</a><br>"
        for site in sites:
            line = site.availability()
            body += line + "<br><br>"
            hashVal = hashlib.sha1(repr(line).encode('utf-8'))
            aggregateHash += hashVal.hexdigest()
        body + "</p>"
        result = hashlib.sha1(repr(aggregateHash).encode('utf-8'))
        state = result.hexdigest()

        #send_email(data['username'], data['password'], data['receivers'], subject, body)
        StateManager.set_state(state,lambda: email(data['username'], data['password'], data['receivers'], subject, body))
    print("STATE: ", StateManager.State)

def poll_availability():
    # create webdriver object
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    while True:
        try:
            # get google.co.in
            driver.get(TURBO_VAX_URL)
            time.sleep(0.2) # Need a fraction of a second for the page to execute js 
            result = driver.find_element_by_css_selector('div.MuiBox-root.jss14')
            status = result.text.replace('(', '') 
            status = result.text.replace(')', '')
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
    
    """
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
            time.sleep(5)

        except KeyboardInterrupt:
            session.close()
            sys.exit()
    """

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
