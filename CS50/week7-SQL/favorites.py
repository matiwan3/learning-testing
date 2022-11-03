import csv
import re

languages = {}

with open("CS50.csv", "r") as file:
    reader = csv.DictReader(file)  # DictReader has keys: values, reader
    # next(reader)  # skip first row
    for row in reader:
        language = row["language"].strip().upper()
        if not language in languages:
            languages[language] = 0
        languages[language] += 1
            
# def get_value(language):
#     return languages[language]

for language in sorted(languages, key=lambda language: languages[language], reverse=True):  # key=get_value
    print(language, languages[language])