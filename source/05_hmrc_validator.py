import requests
import json

def check_hmrc_vat(vat_number):
    """
    Interoghează API-ul public HMRC pentru a valida un număr de VAT britanic.
    """
    # Curățăm numărul de spații, liniuțe sau literele GB
    clean_vat = ''.join(filter(str.isdigit, str(vat_number)))
    
    if len(clean_vat) != 9:
        print(f"[!] Numărul {clean_vat} nu are 9 cifre.")
        return None

    # Endpoint-ul public HMRC
    url = f"https://api.service.hmrc.gov.uk/organisations/vat/check/{clean_vat}"
    headers = {
        "Accept": "application/vnd.hmrc.1.0+json"
    }
    
    print(f"Interogăm HMRC API pentru VAT-ul: {clean_vat}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("\n[SUCCES] Număr VALID conform HMRC!")
            print(f"Companie Înregistrată: {data.get('target', {}).get('name', 'N/A')}")
            
            address = data.get('target', {}).get('address', {})
            addr_string = ", ".join([v for k, v in address.items() if v])
            print(f"Adresă: {addr_string}\n")
            return data
            
        elif response.status_code == 404:
            print(f"\n[X] RESPINS: Numărul {clean_vat} nu există în baza de date HMRC.\n")
            return None
        else:
            print(f"\n[!] Eroare API: Status Code {response.status_code}\n")
            return None
            
    except Exception as e:
        print(f"\n[!] Eroare de conexiune cu HMRC: {e}\n")
        return None

def main():
    print("--- Veridion PoC: HMRC Validation Module ---")
    
    # 1. Testăm cu numărul real de la Waterstones (pe care nu am putut să-l scrapuim, dar știm că e real)
    print("\nTest 1: Validare număr real (Waterstones Booksellers)")
    waterstones_vat = "GB 216 4381 22"
    check_hmrc_vat(waterstones_vat)
    
    # 2. Testăm cu un număr fals generat aleatoriu pentru a demonstra evitarea "False-Positives"
    print("Test 2: Validare număr inventat")
    fake_vat = "999888777"
    check_hmrc_vat(fake_vat)

if __name__ == "__main__":
    main()