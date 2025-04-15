import requests
import fitz  # PyMuPDF
from io import BytesIO

# URL do PDF-a
pdf_url = "https://storage.pdfendpoint.com/46cd30da-472d-47d8-9b9b-d8b60510391a/central-lime-magpie-v8ud52.pdf"

# Pobranie pliku
response = requests.get(pdf_url)
response.raise_for_status()  # sprawdzenie błędu HTTP

# Wczytanie PDF z pamięci
pdf_data = BytesIO(response.content)
doc = fitz.open(stream=pdf_data, filetype="pdf")

# Wypisanie ilości stron
print(f"📄 Liczba stron: {len(doc)}\n")

# Przechodzimy przez strony i szukamy "nagłówków"
for i, page in enumerate(doc, start=1):
    blocks = page.get_text("dict")["blocks"]
    
    # Zbierzemy największe teksty z górnej części strony jako potencjalne nagłówki
    headers = []
    for block in blocks:
        if block["type"] == 0:  # tylko tekst
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["size"] > 15 and span["bbox"][1] < 200:  # większy font + górna część strony
                        headers.append(span["text"])

    print(f"--- Strona {i} ---")
    if headers:
        for h in headers:
            print(f"🟢 Nagłówek: {h}")
    else:
        print("⚠️ Brak nagłówków znalezionych.")
    print()
