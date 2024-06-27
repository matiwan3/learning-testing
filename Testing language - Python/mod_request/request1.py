import requests

"""
The request module provides a convenient way to send HTTP requests and handle responses in Python. It simplifies the process of making HTTP requests and allows you to interact with web services, APIs, and other HTTP-based resources.

Example:
To make a GET request to a URL and retrieve the response content, you can use the `requests` library:



"""

url = 'https://facebook.com'
response = requests.get(url)
print(response.status_code)
print(response.content) 