import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import re
import urllib3

# Ascundem warning-urile pentru site-urile fără certificat SSL valid
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

input_file = os.path.join('data', 'sample_with_domains.csv')
output_file = os.path.join('data', 'sample_with_extracted_vat.csv')

# Expresie regulată pentru a prinde formate de tipul: "VAT: 123 4567 89", "GB123456789", "VAT No. 123-4567-89"
# Caută cuvântul VAT (sau GB), urmat de maxim 15 caractere non-numerice, apoi fix 9 cifre (cu posibile spații/crtatime între ele)
VAT_REGEX = r'(?i)(?:VAT|GB)[^0-9]{0,15}?([0-9]{3}[\s\-]?[0-9]{4}[\s\-]?[0-9]{2})'

def extract_vat_from_text(text):
    """Caută tipare de numere VAT în textul brut."""
    matches = re.findall(VAT_REGEX, text)
    if matches:
        # Luăm prima potrivire și eliminăm spațiile/cratimele pentru a avea un număr curat de 9 cifre
        clean_match = re.sub(r'[\s\-]', '', matches[0])
        return clean_match
    return None

def scrape_website_for_vat(url):
    """Accesează site-ul și extrage textul pentru a căuta numărul VAT."""
    if not url.startswith('http'):
        url = 'https://' + url
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Timeout scurt ca să nu ne blocăm în site-uri picate
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)
        
        return extract_vat_from_text(text_content)
        
    except Exception as e:
        print(f"      [!] Eroare la accesarea {url}: {type(e).__name__}")
        return None

def main():
    print(f"Încărcăm datele din {input_file}...")
    df = pd.read_csv(input_file)
    
    # Adăugăm coloana nouă
    if 'Extracted_VAT' not in df.columns:
        df['Extracted_VAT'] = None

    # Filtrăm doar companiile pentru care am găsit un website
    targets = df[df['Website'].notna()]
    print(f"Avem {len(targets)} site-uri de vizitat.\n")
    
    found_vats = 0
    for index, row in targets.iterrows():
        company = row['CompanyName']
        url = row['Website']
        print(f"-> Scanăm: {company} ({url})")
        
        vat_number = scrape_website_for_vat(url)
        
        if vat_number:
            df.at[index, 'Extracted_VAT'] = vat_number
            print(f"      [V] GĂSIT POTENȚIAL VAT: {vat_number}")
            found_vats += 1
        else:
            print("      [X] Nu am găsit niciun tipar de VAT pe pagina principală.")
            
    df.to_csv(output_file, index=False)
    print(f"\nScanare finalizată! Am extras {found_vats} numere de VAT.")
    print(f"Rezultatele au fost salvate în {output_file}")

if __name__ == "__main__":
    main()