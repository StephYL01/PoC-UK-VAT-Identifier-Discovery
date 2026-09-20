import pandas as pd
import os
import time
from ddgs import DDGS

# Căile către fișiere
input_file = os.path.join('data', 'sample_500_active_companies.csv')
output_file = os.path.join('data', 'sample_with_domains.csv')

# Lista de site-uri agregatoare pe care le excludem din start
IGNORE_DOMAINS = [
    'companieshouse.gov.uk', 'endole.co.uk', 'companycheck.co.uk', 
    'linkedin.com', 'facebook.com', 'twitter.com', 'zoominfo.com', 
    'bloomberg.com', 'gov.uk', 'find-and-update.company-information',
    'suite.endole.co.uk', 'bizstats.co.uk', 'cbetta.com'
]

def is_valid_domain(url):
    """Verifică dacă URL-ul găsit nu face parte din lista de agregate."""
    for domain in IGNORE_DOMAINS:
        if domain in url.lower():
            return False
    return True

def find_company_website(company_name):
    """Caută pe web site-ul oficial al companiei."""
    query = f'"{company_name}" UK official website'
    
    try:
        # Inițializăm căutarea cu DuckDuckGo
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region='uk-en', max_results=5))
            
            for res in results:
                url = res.get('href', '')
                if url and is_valid_domain(url):
                    return url # Returnăm primul rezultat valid
    except Exception as e:
        print(f"  [!] Eroare la căutarea pt {company_name}: {e}")
    
    return None

def main():
    print(f"Încărcăm datele din {input_file}...")
    df = pd.read_csv(input_file)
    
    # Pentru testare, luăm doar primele 20 de companii să nu primim ban pe IP
    test_df = df.head(20).copy()
    test_df['Website'] = None
    
    print("Începem căutarea domeniilor web (adăugăm delay de 2 secunde pentru a evita rate-limiting)...\n")
    
    found_count = 0
    for index, row in test_df.iterrows():
        company_name = row['CompanyName']
        print(f"Căutăm: {company_name}...")
        
        website = find_company_website(company_name)
        
        if website:
            test_df.at[index, 'Website'] = website
            print(f"  -> Găsit: {website}")
            found_count += 1
        else:
            print("  -> Nu am găsit un domeniu valid.")
            
        # Delay crucial pentru a mima comportamentul uman și a nu bloca API-ul
        time.sleep(2)
        
    # Salvăm rezultatele
    test_df.to_csv(output_file, index=False)
    print(f"\nFinalizat! Am găsit site-uri potențiale pentru {found_count} din 20 companii.")
    print(f"Datele au fost salvate în {output_file}")

if __name__ == "__main__":
    main()