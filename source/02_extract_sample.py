import pandas as pd
import os

input_file = os.path.join('data', 'BasicCompanyDataAsOneFile-2026-09-01.csv')
output_file = os.path.join('data', 'sample_500_active_companies.csv')

print(f"Încărcăm datele din {input_file} (poate dura din cauza dimensiunii)...")

try:
    # 1. Citim doar primul rând (header-ul) pentru a prelua numele EXACTE ale coloanelor
    df_header = pd.read_csv(input_file, nrows=0)
    actual_columns = df_header.columns.tolist()
    
    # 2. Căutăm dinamic coloanele noastre, ignorând eventualele spații în plus din CSV
    col_name = next(c for c in actual_columns if 'CompanyName' in c)
    col_number = next(c for c in actual_columns if 'CompanyNumber' in c)
    col_status = next(c for c in actual_columns if 'CompanyStatus' in c)
    col_category = next(c for c in actual_columns if 'CompanyCategory' in c)
    
    exact_cols_to_use = [col_name, col_number, col_status, col_category]
    print(f"Numele exacte detectate în fișier sunt: {exact_cols_to_use}")
    
    # 3. Citim fișierul masiv folosind numele detectate
    df = pd.read_csv(input_file, usecols=exact_cols_to_use, low_memory=False)
    
    # 4. Filtrăm companiile active (folosind denumirea exactă a coloanei de status)
    active_df = df[df[col_status] == 'Active']
    
    # 5. Extragem 500 de companii reproductibil
    sample_df = active_df.sample(n=500, random_state=42)
    
    # 6. Redenumim coloanele eșantionului curat pentru a nu ne bate capul cu spații la partea de scraping
    sample_df.columns = ['CompanyName', 'CompanyNumber', 'CompanyStatus', 'CompanyCategory']
    
    sample_df.to_csv(output_file, index=False)
    print(f"Succes! Am extras {len(sample_df)} companii active și le-am salvat în {output_file}.")

except StopIteration:
    print("Eroare: Nu am putut identifica automat toate cele 4 coloane necesare în fișier.")
except FileNotFoundError:
    print(f"Eroare: Nu am putut găsi {input_file}.")