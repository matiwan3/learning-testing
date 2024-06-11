import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"likes": 10, "name": "Tim", "views": 1000000}, 
    {"likes": 10213, "name": "How to make REST API", "views": 80000}, 
    {"likes": 101, "name": "Ola", "views": 428192974}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
reposnse = requests.get(BASE + "video/0")
print(response.json())
input()
response = requests.get(BASE + "video/2")
print(response.json())