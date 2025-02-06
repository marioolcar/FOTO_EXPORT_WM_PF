# https://docs.google.com/spreadsheets/d/1oBPT3FXSs9tqJvfsU3FjxIyKUvhgHWmMVfcYB4vywYM/gviz/tq?tqx=out:csv&sheet=Koncerti



import pandas as pd
import unidecode

#pd.options.display.max_rows = 999
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)



SHEET_ID = "1oBPT3FXSs9tqJvfsU3FjxIyKUvhgHWmMVfcYB4vywYM"
SHEET_NAME = "Koncerti"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

df = pd.read_csv(CSV_URL,  encoding='utf-8')

def formatiraj_koncert(koncert):
    if pd.isna(koncert):  # Ako je NaN ili None, vrati ga bez promjene
        return koncert
    # Zamjena razmaka s '_', pretvaranje u mala slova, uklanjanje dijakritičkih znakova
    koncert = unidecode.unidecode(koncert)  # Ukloni dijakritičke znakove
    koncert = koncert.lower()  # Pretvori u mala slova
    koncert = ''.join(e for e in koncert if e.isalnum() or e == ' ')
    koncert = ' '.join(koncert.split())  # Zamijeni višestruke razmake s jednim
    koncert = koncert.replace(" ", "_")  # Zamijeni razmake s '_'

    # Uklanjanje specijalnih znakova (ostavljanje samo slova, brojeva i donjih crta)
    return koncert

def formatiraj_datum(datum):
    # Pretpostavljamo da datum dolazi u formatu koji možeš pretvoriti u YYYYMMDD
    datum = pd.to_datetime(datum, errors='coerce', dayfirst=True)  # Pretvori u datetime, zanemari pogrešne formate
    if pd.isna(datum):  # Ako datum nije validan, vrati prazan string
        return ""
    return datum.strftime('%Y%m%d')  # Vratiti datum u obliku YYYYMMDD

def formatiraj_tehnika(tehnika):
    tehnika = tehnika.replace("Analogno", "a")
    tehnika = tehnika.replace("Digitalno", "d")
    return tehnika

def formatiraj_fotograf(koncert):
    if pd.isna(koncert):  # Ako je NaN ili None, vrati ga bez promjene
        return koncert
    
    koncert = unidecode.unidecode(koncert)  # Ukloni dijakritičke znakove
    koncert = koncert.lower()  # Pretvori u mala slova
    koncert = koncert.replace(" ", "_")  # Zamijeni razmake s '_'
    

    return koncert

# Primjeni funkcije na odgovarajuće stupce
rezultat = df.loc[:, ["Koncert", "Datum", "Fotograf", "Tehnika"]]
rezultat['Datum'] = rezultat['Datum'].apply(formatiraj_datum)
rezultat['Koncert'] = rezultat['Koncert'].apply(formatiraj_koncert)
rezultat['Tehnika'] = rezultat['Tehnika'].apply(formatiraj_tehnika)
rezultat['Fotograf'] = rezultat['Fotograf'].apply(formatiraj_koncert)

# Spoji Datum i Koncert u jedan stupac u željenom formatu
rezultat['Spojeni'] = rezultat['Datum'] + "_" + rezultat['Koncert'] + "_" + rezultat['Tehnika'] + "_" + rezultat['Fotograf']


#print(rezultat)

with open("rezultat.txt", "w",  encoding='utf-8') as file:
    file.write(rezultat.to_string())
