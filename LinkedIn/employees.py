# Import libraries and packages for the project 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
import requests
import pandas as pd

print('- Finish importing packages')

def login():
      sleep(2)
      url = 'https://www.linkedin.com/login'
      driver.get(url)
      print('- Finish initializing a driver')
      sleep(1)

      # Task 1.2: Import username and password
      credential = open('credentials.txt')
      line = credential.readlines()
      username = line[0]
      password = line[1]
      print('- Finish importing the login credentials')
      sleep(1)

      # Task 1.2: Key in login credentials
      email_field = driver.find_element_by_id('username')
      email_field.send_keys(username)
      print('- Finish keying in email')
      sleep(3)

      password_field = driver.find_element_by_name('session_password')
      password_field.send_keys(password)
      print('- Finish keying in password')
      sleep(2)

      # Task 1.2: Click the Login button
      signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
      signin_field.click()
      sleep(1.5)

      print('- Finish Task 1: Login to Linkedin')


def search(key=''):
    search_field = driver.find_element_by_class_name('search-global-typeahead__input')
    # Task 2.2: Input the search query to the search bar
    keyword = key + ' ' + 'people'
    search_field.send_keys(keyword)

    # Task 2.3: Search
    search_field.send_keys(Keys.RETURN)
    sleep(3)
    print('- Finish Task 2: Search for profiles')
    try:
        see_full_result = driver.find_element_by_css_selector('#main > div > div > div:nth-child(1) > div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a')
        see_full_result.click()
    except:
        print('CANNOT CLICK')
        
    



# Task 3.1: Write a function to extract the URLs of one page
def GetURL():
    page_source = BeautifulSoup(driver.page_source)
    profiles = page_source.find_all('a', class_ = 'app-aware-link')
    all_profile_URL = []
    for profile in profiles:
        profile_ID = profile.get('href')
        profile_URL = profile_ID.split('?')[0].split('/')[4]
        if profile_URL not in all_profile_URL:
            all_profile_URL.append(profile_URL)
    return all_profile_URL


def FullURL():
    input_page = 10
    URLs_all_page = []
    for page in range(input_page):
        URLs_one_page = GetURL()
        # print(URLs_one_page)
        sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
        sleep(3)
        # next_button = driver.find_element_by_class_name("artdeco-pagination__button--next")
        try:
            next_button = driver.find_element_by_css_selector('[aria-label=Next]')
        except:
            print("Error when Loading")
            driver.refresh()
            continue
            
        driver.execute_script("arguments[0].click();", next_button)
        URLs_all_page = URLs_all_page + URLs_one_page
        sleep(3)
    return URLs_all_page

def read_csv(file_name):
      df = pd.read_csv(file_name,header=None)
      list = df[0].tolist()
      return list




# DRIVER_PATH = '../driver/mac/chromedriver'
DRIVER_PATH = '../driver/linux/chromedriver_linux64/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.maximize_window()

def main():
    login()
    # list_keywords = read_csv('search_keywords.csv')
    # for key in list_keywords:
    #     search(key)
    #     sleep(1.5)
    #     url_employees = FullURL()
    #     df = pd.DataFrame(url_employees)
    #     output_path = './users_result/' + key + '.csv'
    #     df.to_csv(output_path, mode='a', header=False, index=False)
    #     driver.get('https://www.linkedin.com')
    keyword = 'Tester'
    search(keyword)
    url_employees = FullURL()
    print(url_employees)
    
main()