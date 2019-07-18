
#https://drd.sh/4NsxpG/
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import random
from collections import OrderedDict
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import string
from datetime import datetime

class Dashbot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.6 Safari/537.36')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    #links to spreadsheet where the accounts are stored
    def record_acc(self,email,password):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('accounts.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open("dash bot").sheet1

        now = datetime.now() 
        d = now.strftime("%m/%d/%Y")

        account_num = int(sheet.cell(2,6).value)

        account = [email, password, d]
        sheet.insert_row(account,account_num+2)

    def generate(self):
        
        
        first_names = ["James",'Harry','John','Brandon','Ryan','Kevin','Chris','Richard', 'Louis', 'Jacob']
        last_names = ['Lee','Oh','Park','Bom','Chen','Lu','Kim', 'Jung','Choi']

        #referal_link = input("enter referal link: ")

        self.driver.get("https://drd.sh/ZeDvbN/")
        try:
            # wait for input to load
            firstname_input = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ConsumerApp"]/div/div[1]/div/div[5]/div/section[1]/div/div/div/div[2]/form/label[1]/input'))
                )
        except TimeoutException:
            return
        lastname_input = self.driver.find_element_by_xpath(
            '//*[@id="ConsumerApp"]/div/div[1]/div/div[5]/div/section[1]/div/div/div/div[2]/form/label[2]/input')
        email_input = self.driver.find_element_by_xpath(
            '//*[@id="ConsumerApp"]/div/div[1]/div/div[5]/div/section[1]/div/div/div/div[2]/form/label[3]/input')
        mobile_input = self.driver.find_element_by_xpath(
            '//*[@id="ConsumerApp"]/div/div[1]/div/div[5]/div/section[1]/div/div/div/div[2]/form/label[4]/input')
        password_input = self.driver.find_element_by_xpath(
            '//*[@id="ConsumerApp"]/div/div[1]/div/div[5]/div/section[1]/div/div/div/div[2]/form/span/div/label/div[3]/input')
        
        #generate random email and password
        email = '{}@gmail.com'.format(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4)))
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

        #send values to inputs
        firstname_input.send_keys(first_names[random.randint(0,len(first_names)-1)])
        lastname_input.send_keys(last_names[random.randint(0,len(last_names)-1)])
        email_input.send_keys(email)
        password_input.send_keys(password)
        
        mobile = input("enter mobile number: ")
        
        mobile_input.send_keys(mobile)

        submit_button = self.driver.find_element_by_xpath(
            '//*[@id="ConsumerApp"]/div/div[1]/div/div[5]/div/section[1]/div/div/div/div[2]/form/button').click()
        
        #wait for code input to appear
        try:
            code_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ConsumerApp"]/div/div[1]/div/div[5]/div/div/div/div/div/div/div[2]/label/div/input')))
        except TimeoutException:
            print("[-] Error")
            return
        
        code = input("enter confirmation code: ")
        code_input.send_keys(code)
        code_button = self.driver.find_element_by_xpath(
            '//*[@id="ConsumerApp"]/div/div[1]/div/div[5]/div/div/div/div/div/div/div[2]/button').click()
        
        self.record_acc(email,password)

        print("Done! \n" +"email:" + email + "\npassword:" + password)
        self.driver.delete_all_cookies()





bot = Dashbot()
bot.generate()
time.sleep(5)

print("compiled")