"""
SOURCE1: https://realpython.com/beautiful-soup-web-scraper-python/
SOURCE2: https://towardsdatascience.com/web-scraping-metacritic-reviews-using-beautifulsoup-63801bbe200e
Apps Script web scraper: https://medium.com/@interdigitizer/scrape-and-save-data-to-google-sheets-with-apps-script-7e3c0ccec96b
BeautifulSoup scraper: https://pypi.org/project/beautifulsoup4/
BautifulSoup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
Navigating fields with selenium: https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
Selenium docs: https://selenium-python.readthedocs.io/getting-started.html
Quick & Easy Selenium+Pandas+BS example: https://towardsdatascience.com/in-10-minutes-web-scraping-with-beautiful-soup-and-selenium-for-data-professionals-8de169d36319
"""

# Imports
import requests
from bs4 import BeautifulSoup
import re
import string
import numpy as np
import warnings
import time

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# BAD PRACTICE. Just for nice output.
warnings.filterwarnings("ignore")

# Define Vars:
home_url = 'http://tmsearch.uspto.gov/#'
# user_agent = {'User-agent': 'Mozilla/5.0'}
# request_url = base_url + str(page_index)

driver = webdriver.Chrome(executable_path='chromedriver')
# Enable to implicitly wait before handing back control.
driver.implicitly_wait(1)

# Page navigation
tm_search = 'Nova'
timeout = 3  # how long to wait for page to load.
max_index = 1
session_id = ''

# Data Arrays
serial_numbers = []
goods_and_services = []
word_marks = []

debug = True

# Define Functions:


def driverWait_Tag(tag):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.TAG_NAME, tag)))
        if debug:
            print('found element by tag: {}'.format(tag))
    except TimeoutException:
        if debug:
            print('no element tag found \' {} \', quitting.'.format(tag))
        driver.quit()


def driverWait_ID(id):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, id)))
        if debug:
            print('found element by ID: {}'.format(id))
    except TimeoutException:
        if debug:
            print('no element id found \' {} \', quitting.'.format(id))
        driver.quit()


def getSessionID():
    # Once you start your session in the USPTO trademark search, grabs the sessionID from the http address so you can navigate easier.
    url = driver.current_url
    session_id = url.split('&')[1].rstrip(
        '1.1#')  # remove last number so we can iterate over entries
    if debug:
        print(session_id)
    return session_id


def clickLinkText(text):
    driverWait_Tag('a')  # make sure we've actually loaded a link.
    elem = driver.find_element_by_link_text(text)
    elem.click()
    if debug:
        print("clicked!")
    return


def getResultCount():
    # After you kickoff your search, you will snag the number of entries to index over.
    return


def startSearch(trademark, live_only):
    # Start the USPTO search.
    if live_only:
        try:
            elem = driver.find_element_by_xpath("//input[@value='live']")
            elem.click()
        except:
            print("Xpath failed at live")
            driver.quit()

    try:
        elem = driver.find_element_by_xpath(
            "//input[@type = 'text' and @name = 'p_s_PARA2']")
        elem.send_keys(trademark)  # fill in the search field
    except:
        print("Xpath failed at keys")
        driver.quit()

    try:
        elem = driver.find_element_by_xpath(
            "//input[@type='SUBMIT' and @value='Submit Query']")
        elem.click()
    except:
        print("Xpath failed at submit")
        driver.quit()


def getMaxIndex():
    # USPTO lists max index - grab it so we can iterate.
    elem_text = driver.find_element_by_xpath(
        "//font[@size = '+2' and @color = 'blue']").text

    index = int(elem_text.split(' ')[0])
    if debug:
        print("index = {}".format(index))
    return index


def goToIndex(index, session_id):
    # Access the first entry in the search list.

    base_url = "http://tmsearch.uspto.gov/bin/showfield?f=doc&"
    # formatting is weird, is how it is.
    url = base_url + session_id + '.2.' + str(index)
    print('target url: ' + url)
    driver.get(url)
    return


def pull_Data(request_url):
    # Data in USPTO site is stored in tables. The 4th table (index 3) on each page contains the relevant data.

    # table = soup.find_all('table')[3]
    return soup


# Test
# if (printout):
#     print(pull_Data(request_url))


# Script

# while (page_index < 1393):
#     page_index += 11

def main():
    # Start up Selenium
    driver.get(home_url)  # Load USPTO start page.
    print(driver.current_url)
    session_id = getSessionID()  # Unique session ID

    # Start search
    clickLinkText('Basic Word Mark Search (New User)')
    startSearch(tm_search, True)
    max_index = getMaxIndex()

    # Access entries
    for i in range(5):
        goToIndex(i+1, session_id)

    time.sleep(10)
    driver.quit()


if __name__ == "__main__":
    # Standard sytnax
    main()
