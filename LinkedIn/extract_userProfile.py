from numpy import insert
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
import requests
import pymongo


def login():
      sleep(2)
      url = 'https://www.linkedin.com/login'
      driver.get(url)
      print('- Finish initializing a driver')
      sleep(1)

      # Task 1.2: Import username and password
      credential = open('credentials.txt',encoding="utf8")
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
      # sleep(3)

      # Task 1.2: Click the Login button
      # signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
      # signin_field.click()
      # sleep(1.5)

      print('- Finish Task 1: Login to Linkedin')

      # Task 1.3: Check if the login is successful

def getUserProfile(id=''):
    driver.get('https://www.linkedin.com/in/' + id)
    name = ''
    role = ''
    name = driver.find_elements_by_class_name('text-heading-xlarge')[0].text

    role = driver.find_element_by_css_selector('#ember37 > div.ph5 > div.mt2.relative > div:nth-child(1) > div.text-body-medium.break-words').text
    # print(role)
    sleep(3)
    skill_list = getSkills(id)
    # sleep(2)
    return name,role,skill_list


def getExperience(id=''):
    driver.get('https://www.linkedin.com/in/' + id +'/details/experience')
    experience = []
    page_source =  BeautifulSoup(driver.page_source,'html.parser')
    
    list_experience = page_source.select('div.display-flex.flex-row.justify-space-between')
    # print("LENGTH: ", len(list_experience))

    count = 0
    for item in list_experience:
        item_hidden = item.find_all('span',{'aria-hidden':'true'})
        count += 1
        # print("COUNT: ", count)
        exp = ''
        for i in item_hidden:
            exp = exp + i.text + ','
        exp = exp[:-1]
        experience.append(exp)
    skill_list = getSkills(id)
    return experience,skill_list

def getEducation(id=''):
    driver.get('https://www.linkedin.com/in/' + id +'/details/education')
    education = []
    page_source =  BeautifulSoup(driver.page_source,'html.parser')
    
    list_experience = page_source.select('div.display-flex.flex-row.justify-space-between')
    # print("LENGTH: ", len(list_experience))

    count = 0
    for item in list_experience:
        item_hidden = item.find_all('span',{'aria-hidden':'true'})
        count += 1
        # print("COUNT: ", count)
        exp = ''
        for i in item_hidden:
            exp = exp + i.text + ','
        exp = exp[:-1]
        education.append(exp)
    
    skill_list = getSkills(id)
    return education,skill_list


def getSkills(id=''):
    driver.get('https://www.linkedin.com/in/' + id +'/details/skills')
    # sleep(0.2)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated 
    sleep(0.6)
    skill_list = []
    page_source =  BeautifulSoup(driver.page_source,'html.parser')
    list_skill = page_source.select('span.mr1.t-bold')
    # print("LENGTH: ", len(list_skill))
    
    for item in list_skill:
        # print(item)
        item_list = item.find_all('span',{'aria-hidden':'true'})
        
        # print(item_list)
        for i in item_list:
            if i.text not in skill_list:
                skill_list.append(i.text)
    # print(skill_list)
    return skill_list

# Connect to Mongo DB
def connect():
    url='mongodb://mongoadmin:admin@13.67.48.201:27017/'
    myclient = pymongo.MongoClient(url)
    return myclient


def read_user_mongodb(myclient:pymongo.MongoClient):
    # Connect to MongoDB
    # Return list of userID
    import pandas as pd
    mydb = myclient['LinkedIn']
    mycol = mydb['UserIDs']
    mydoc = mycol.find() 
    result = list(mydoc)
    user_id_list = [item['_id'] for item in result]
    # df = pd.DataFrame(result['_id'])
    return user_id_list

def insert_a_record(myclient:pymongo.MongoClient,db='LinkedIn',collection='User_skills_profiles',data={}):
    mydb = myclient[db]
    mycol = mydb[collection]
    mycol.insert_one(data)

print('- Finish importing packages')
# DRIVER_PATH = '../driver/mac/chromedriver'
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.maximize_window()

if __name__ == '__main__':
    #db connection
    myclient = connect()
    user_id_list = read_user_mongodb(myclient)
    count_users = len(user_id_list)
    login()
    sleep(2)
    for i in range(133,233):
        sleep(3)
        print("User number: ",i)
        name=''
        role = ''
        skills = []
        try:
            skills = getSkills(user_id_list[i])
        except:
            print("ERROR at ID: ",user_id_list[i])

        dict_user = {'_id':user_id_list[i],'name':name,'role':role,'skills':skills}
        print(dict_user)
        insert_a_record(myclient,'LinkedIn','User_skills_profiles',dict_user)
    # name,role,skills = getUserProfile(user_id_list[113])
    # dict_user = {'_id':user_id_list[i],'name':name,'role':role,'skills':skills}
    # print(dict_user)
    driver.close()