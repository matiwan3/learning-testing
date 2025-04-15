# 1. Otwórz aplikację (Selenium)
# 2. Zaloguj się, wykonaj akcję generującą PDF (np. kliknij „Export PDF”)
# 3. Pobierz link do pliku PDF
# 4. Pobierz plik PDF do testu (requests)
# 5. Sparsuj i przeanalizuj PDF (PyPDF2/pdfminer)
# 6. Sprawdź, czy zawiera oczekiwane dane (asercje)

# test_pdf.py
# -*- coding: utf-8 -*-
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import PyPDF2

driver = webdriver.Chrome()
driver.get("https://app.example.com")

# Login & navigate
driver.find_element(By.ID, "username").send_keys("test_user")
driver.find_element(By.ID, "password").send_keys("secure123")
driver.find_element(By.ID, "login").click()

# Generate PDF
driver.find_element(By.ID, "generate-pdf").click()
time.sleep(5)

# Get PDF URL
pdf_link = driver.find_element(By.LINK_TEXT, "Download PDF").get_attribute("href")

# Download PDF
pdf_response = requests.get(pdf_link)
with open("report.pdf", "wb") as f:
    f.write(pdf_response.content)

# Parse PDF
with open("report.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    text = reader.pages[0].extract_text()

# Assert
assert "Invoice ID" in text
assert "test_user" in text

driver.quit()
