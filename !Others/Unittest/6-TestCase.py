import unittest
from selenium import webdriver
import time


class FacebookTest(unittest.TestCase):
    def setUp(self):
        self.facebook = "https://facebook.com"
        self.path_chrome = r'../driver-chrome.exe'
        self.driver = webdriver.Chrome(self.path_chrome)
        # to supress the error messages/logs
        self.options = webdriver.ChromeOptions() 
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options, executable_path=self.path_chrome)
        self.driver.get(self.facebook)
        
    def test_title(self):
        time.sleep(2)
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
