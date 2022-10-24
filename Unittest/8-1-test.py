import json
import requests
import time
import os

stack_url = 'https://api.stackexchange.com//2.3/questions?order=desc&sort=activity&site=stackoverflow'
response = requests.get(stack_url)
response_info = (response.json())
users_list = []
names_counter = 0

with open('8-1-1-list-of-users.txt', 'a', encoding="utf-8") as f:
    f.write('List of users: ')
    for info in response_info['items']:
        users_list.append(info['owner']['display_name'])
        names_counter += 1
        f.write(info['owner']['display_name'] + ", ")
        if names_counter % 9 == 0:
            f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()
        # print(users_list)
        




   