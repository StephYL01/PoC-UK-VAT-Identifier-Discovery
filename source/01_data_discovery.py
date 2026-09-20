import pandas as pd

# Calea către fișierul brut
file_path = r"D:\Veridion_Proof_of_Concept\data\BasicCompanyDataAsOneFile-2026-09-01.csv"

try:
    # Citim exclusiv primele 5 rânduri (nrows=5)
    df_sample = pd.read_csv(file_path, nrows=5)
    
    print("Coloanele disponibile sunt:\n")
    for col in df_sample.columns:
        print(f"- {col}")
        
    print("\nDatele primei companii:")
    # Afișăm valorile primului rând (index 0) pentru a vedea formatul real
    print(df_sample.iloc[0])

except Exception as e:
    print(f"Eroare la citire: {e}")