import unittest
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
from datetime import datetime

class TitleTest(unittest.TestCase):
    def setUp(self):
        self.stack_url = 'https://api.stackexchange.com//2.3/questions?order=desc&sort=activity&site=stackoverflow'
        self.response = requests.get(self.stack_url)
        self.response_info = (self.response.json())
    
    def test_title(self):
        title_list = []
        try:
            for info in self.response_info['items']:
                title_list.append(info['title'])
        except KeyError:
            print("Key Error occured")
            
    def test_users(self):
        users_list = []
        names_counter = 0
        self.now = datetime.now()
        dt_string = self.now.strftime("%d/%m/%Y %H:%M:%S")
        try:
            self.assertIn('items', self.response_info)  
            with open('8-1-1-list-of-users.txt', 'a', encoding="utf-8") as f:
                f.write(f'{dt_string} ; List of users: ')
                for info in self.response_info['items']:
                    users_list.append(info['owner']['display_name'])
                    names_counter += 1
                    f.write(info['owner']['display_name'] + ", ")
                    if names_counter % 9 == 0:
                        f.write('\n')
                f.write('\n')
                f.write('\n')
                f.close()
        # Be careful of: too many requests from this IP, more requests available in x seconds
        except KeyError:
            print("Key Error")
        
    def test_truth(self):
        simple_string = 'Today is a sunny day'
        a = 5
        b = 25/5 
        c = 31
        self.assertEqual(a,b)
        self.assertLess(a,c)
        self.assertRegex(simple_string,'sunny')
    
    def test_email_in_page(self):
        pizza_url = 'https://www.pizzeria-mario.pl/kontakt#/r=pizzeria-mario-winogrady'
        self.chrome_path = '../driver-chrome.exe'
        s=Service(self.chrome_path)
        self.options = webdriver.ChromeOptions() 
        self.options.add_argument('--headless')  # also works self.driver.minimize_window()
        self.options.add_argument('--disable-gpu')  # disables GPU
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options, service=s)
        self.driver.get(pizza_url)

        element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'main'))
        )
        p_s = self.driver.page_source
        self.assertRegex(p_s, r"[\d]{3}-[\d]{3}-[\d]{3}")

    def test_randint_equal(self):
        unsorted_list = []
        for _ in range(50):
            unsorted_list.append(randint(1,1000))

        sorted_list = sorted(unsorted_list)
        # print(f'{unsorted_list}\n{sorted_list}')
        self.assertCountEqual(unsorted_list, sorted_list)
        assert len(sorted_list) == 50
        
    def test_lambda_operations(self):
        x = lambda x,y : x * y
        self.assertEqual((x(5, 9)),45) 
        
    def teardown(self):
        self.driver.close()
           
if __name__ == "__main__":
    unittest.main()
            
            
        
        