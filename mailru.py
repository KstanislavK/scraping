import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv('../.env')

HOST = 'localhost'
PORT = 27017
DB = 'mail_box'
COL = 'mail0607'

LOGIN = os.environ.get('LOGIN')
PASS = os.environ.get('PASS')
URL = 'https://mail.ru/'

driver = webdriver.Firefox('C:/Users/Stas/PycharmProjects/parcing/lesson_5')
driver.set_window_size(1920,1080)
driver.get(URL)


log_elem = driver.find_element_by_name('login')
log_elem.send_keys(LOGIN)
log_elem.send_keys(Keys.ENTER)

pass_elem = WebDriverWait(driver, 10)
pass_elem.until(expected_conditions.visibility_of_element_located((By.NAME, 'password')))

pas_elem = driver.find_element_by_name('password')
pas_elem.send_keys(PASS)
pas_elem.send_keys(Keys.ENTER)

email_list = WebDriverWait(driver, 10)
email_list.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')))

link_all = set()
email_list = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
link_list = list(map(lambda el: el.get_attribute('href'), email_list))
link_all = link_all.union(set(link_list))

while True:
    last_mail = email_list[-1]
    actions = ActionChains(driver)
    actions.move_to_element(last_mail)
    actions.perform()

    time.sleep(5)
    email_list = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')

    link_list = list(map(lambda el: el.get_attribute('href'), email_list))

    if link_list[-1] not in link_all:
        link_all = link_all.union(set(link_list))
        continue
    else:
        break

mail_list = driver.find_elements_by_class_name('js-letter-list-item')

with MongoClient(HOST, PORT) as client:
    db = client[DB]
    letters = db[COL]
    mails = []
    for item in mail_list:
        letter = {
            'from': item.find_element_by_xpath('.//span[@class="ll-crpt"]').get_attribute('title'),
            'subject': item.find_element_by_xpath('.//span[@class="ll-sj__normal"]').text,
            'link': str.split(item.get_attribute('href'), sep='?')[0],
            'time': item.find_element_by_xpath('.//div[@class="llc__item llc__item_date"]').get_attribute('title'),
        }
        # letters.insert_one(letter)
        mails.append(letter)
    letters.insert_many(mails)
    print('ok')
