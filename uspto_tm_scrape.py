# Imports
import requests
import re
import string
import pandas as pd
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

# Define Global Vars:
home_url = 'http://tmsearch.uspto.gov/#'

# Page navigation
timeout = 3  # how long to wait for elements to load with explicit waits.

# Debug Mode for printing.
debug = False

# Define Functions:


def driverWait_Tag(tag, driver):
    # Wait for specific type of tag to load
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.TAG_NAME, tag)))
        if debug:
            print('found element by tag: {}'.format(tag))
    except TimeoutException:
        if debug:
            print('no element tag found \' {} \', quitting.'.format(tag))
        driver.quit()


def driverWait_ID(id, driver):
    # Wait for a particular element ID to appear
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, id)))
        if debug:
            print('found element by ID: {}'.format(id))
    except TimeoutException:
        if debug:
            print('no element id found \' {} \', quitting.'.format(id))
        driver.quit()


def getSessionID(driver):
    # Once you start your session in the USPTO trademark search, grabs the sessionID from the http address so you can navigate easier.
    url = driver.current_url
    session_id = url.split('&')[1].rstrip(
        '1.1#')  # remove last number so we can iterate over entries
    if debug:
        print(session_id)
    return session_id


def clickLinkText(text, driver):
    # Finds and clicks link with exact specified text.
    driverWait_Tag('a', driver)  # make sure we've actually loaded a link.
    elem = driver.find_element_by_link_text(text)
    elem.click()
    if debug:
        print("clicked!")
    return


def startSearch(trademark, live_only, driver):
    # Start the USPTO search.
    if live_only:
        try:
            elem = driver.find_element_by_xpath("//input[@value='live']")
            elem.click()
        except:
            if debug:
                print("Xpath failed at live")
            driver.quit()

    try:
        elem = driver.find_element_by_xpath(
            "//input[@type = 'text' and @name = 'p_s_PARA2']")
        elem.send_keys(trademark)  # fill in the search field
    except:
        if debug:
            print("Xpath failed at keys")
        driver.quit()

    try:
        elem = driver.find_element_by_xpath(
            "//input[@type='SUBMIT' and @value='Submit Query']")
        elem.click()
    except:
        if debug:
            print("Xpath failed at submit")
        driver.quit()


def getMaxIndex(driver):
    # USPTO lists max index - grab it so we can iterate.
    elem_text = driver.find_element_by_xpath(
        "//font[@size = '+2' and @color = 'blue']").text

    index = int(elem_text.split(' ')[0])
    if debug:
        print("index = {}".format(index))
    return index


def goToIndex(index, session_id, driver):
    # Access the specified entry in the search list.

    base_url = "http://tmsearch.uspto.gov/bin/showfield?f=doc&"
    # formatting is weird, is how it is.
    url = base_url + session_id + '.2.' + str(index)
    driver.get(url)
    return


def pull_Data(driver):
    # Pulls G&S, Wordmark, Serial data from search entry.
    data_row = []
    match = ['Word Mark', 'Goods and Services', 'Serial Number']
    for i in match:
        text = findTextInTable(i, driver)
        if debug:
            print(text)
        data_row.append(text)

    return data_row


def findTextInTable(target, driver):
    # Unfortunately the table formatting is not consistent, so you need to iterate through the table until you find the data.
    # TODO: Can reduce time significantly by iterating only once and pulling data as you come across it, rather than going through for each item.
    try:
        rows = driver.find_elements_by_xpath("//table[5]/tbody/tr")
        for i in range(len(rows)):
            cols = rows[i].find_elements_by_xpath(
                "//table[5]/tbody/tr[{}]/td".format(i))
            for j in range(len(cols)):
                test = cols[j].text
                if test == target:
                    return cols[j+1].text
    except Exception as e:
        print(e)
        driver.quit()


def exportCSV(data):
    df = pd.DataFrame(data, columns=['Word Mark', 'G & S', 'Serial #'])
    df.to_csv('test_data.csv')
    return


def runSearch(search_term):
    # Runs your search, saves to pandas DF
    data_list = list()

    # Start up Selenium
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.implicitly_wait(1)

    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1200x600')

    driver.get(home_url)  # Load USPTO start page.
    print(driver.current_url)
    session_id = getSessionID(driver)  # Unique session ID

    # Start search
    clickLinkText('Basic Word Mark Search (New User)', driver)
    startSearch(search_term, True, driver)
    max_index = getMaxIndex(driver)

    # Access entries
    for i in range(max_index):
        if debug:
            print("index: {}".format(i+1))
        goToIndex(i+1, session_id, driver)
        data_row = pull_Data(driver)
        data_list.append(data_row)

    driver.quit()

    return data_list


def getSearchTerm():
    print("\n Which term would you like to search for?")
    tm_search = input()

    if not tm_search:
        print('You have failed spectacularly. I will end myself.')
        exit()

    return tm_search


def main():
    search_term = getSearchTerm()
    data_list = runSearch(search_term)
    exportCSV(data_list)
    print("Data Saved!")
    quit()


if __name__ == "__main__":
    main()
