from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Chrome driver version: 135.0.7049.84
# Chrome version: 135.0.2197.91
current_directory = os.path.dirname(os.path.realpath(__file__))  # Bieżący folder skryptu
CHROMEDRIVER_PATH = os.path.join(current_directory, "135-0-7049-84WEBDRIVER.exe")

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Odkomentuj jeśli chcesz uruchamiać w tle (bez GUI)

# Tworzymy Service i WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get("https://google.com")
print("Tytuł strony:", driver.title)

time.sleep(5)  # Czekamy 5 sek żeby zobaczyć co się dzieje

# Zamykamy przeglądarkę
driver.quit()
