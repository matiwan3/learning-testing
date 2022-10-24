import unittest
import requests
import json


class TitleTest(unittest.TestCase):
    def setUp(self):
        self.stack_url = 'https://api.stackexchange.com//2.3/questions?order=desc&sort=activity&site=stackoverflow'
        self.response = requests.get(self.stack_url)
        self.response_info = (self.response.json())
    
    def test_title(self):
        title_list = []
        for info in self.response_info['items']:
            title_list.append(info['title'])
            
    def test_users(self):
        users_list = []
        for info in self.response_info['items']:
            users_list.append(info['owner']['display_name'])
        assert 'Chris' in users_list
    
if __name__ == "__main__":
    unittest.main()
            
            
        
        