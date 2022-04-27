# Import libraries and packages for the project 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs4
from time import sleep
import csv
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd 

# DRIVER_PATH = '../driver/linux/chromedriver_linux64/chromedriver'
DRIVER_PATH = '../driver/mac/chromedriver'
      # Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.maximize_window()

def login():
      sleep(2)
      url = 'https://www.linkedin.com/login'
      driver.get(url)
      print('- Finish initializing a driver')
      sleep(2)

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
      sleep(2.5)

      password_field = driver.find_element_by_name('session_password')
      password_field.send_keys(password)
      print('- Finish keying in password')
      sleep(2.5)

      # Task 1.2: Click the Login button
      signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
      signin_field.click()
      sleep(1)

      print('- Finish Task 1: Login to Linkedin')

      # Task 1.3: Check if the login is successful


def search(key=''):
      search_field = driver.find_element_by_class_name('search-global-typeahead__input')
       
      # Task 2.2: Input the search query to the search bar
      keyword = key + ' ' + 'job'
      search_field.send_keys(keyword)

      # Task 2.3: Search
      search_field.send_keys(Keys.RETURN)
      sleep(3)                                                 
      try:
            # sell_full_result = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[2]')
            sell_full_result = driver.find_element_by_css_selector('#main > div > div > div:nth-child(1) > div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a')
            sell_full_result.click()                                #main > div > div > div:nth-child(2) > div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a
      except:                                                       #main > div > div > div:nth-child(1) > div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a     
            print("CANNOT CLICK")                                   #main > div > div > div:nth-child(1) > div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a
            pass                                                    #main > div > div > div:nth-child(2) > div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a
                                                                    #main > div > div > div:nth-child(1) > div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a  

# print('- Finish Task 2: Search for profiles')


def GetURL(key=''):
      sleep(4)
      for i in range(10):
            x = 500*i
            driver.execute_script("document.getElementsByClassName('jobs-search-results-list')[0].scrollTo(0,{});".format(x))
            sleep(0.5)

      profiles = driver.find_elements_by_class_name('job-card-list__title')
      print('LENGTH:', len(profiles))
      all_profile_URL = []
      for profile in profiles:
            profile_ID = profile.get_attribute('href')
            profile_name = profile.text
            if profile_name.find(key) != -1:
                  print("Job Title: ",profile_name)
                  profile_URL = profile_ID.split('?')[0].split('/')[5]
                  if profile_URL not in all_profile_URL:
                        all_profile_URL.append(profile_URL)
      return all_profile_URL


def FullURL(keyword=''):
      input_page = 40
      URLs_all_page = []
      for page in range(1,input_page):
            # Get url from 1 page
            URLs_one_page  =  GetURL(key=keyword)
            URLs_all_page = URLs_all_page + URLs_one_page            
            # Go to Next page
            next_page = "Page " + str(page+1)
            try:
                  next_button = driver.find_element_by_css_selector('[aria-label="{}"]'.format(next_page))
            except:
                  print("ERROR: No Next Page")
                  driver.refresh()
                  continue
            driver.execute_script("arguments[0].click();", next_button)
      
      return URLs_all_page

def read_csv(file_name):
      df = pd.read_csv(file_name,header=None)
      list = df[0].tolist()
      return list


def main():
      login()
      list_key = read_csv('./search_keywords.csv')
      for item in list_key:
            search(item)
            sleep(3)
            url_jobs = FullURL(item)

            import pandas as pd 
            df = pd.DataFrame(url_jobs)
            output_result = './jobs_result/' + item + '.csv'
            df.to_csv(output_result,mode='a', header=False)
            driver.get('https://www.linkedin.com')

main()