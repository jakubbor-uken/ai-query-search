import os
import json
import glob
import requests
import pandas as pd
from datasets import load_dataset
from transformers import AutoTokenizer


# Część baz danych należy pobrać i umieścić w folderze przed wykonaniem:
# `https://datacatalogfiles.worldbank.org/ddh-published/0037712/DR0095335/WDI_CSV_10_08.zip` - `utilities/wdi_data/...`
#  https://www.kaggle.com/datasets/shivamb/netflix-shows - `utilities/netflix_titles.csv`

# ---------------------------
# UŻYWAMY OTWARTEGO TOKENIZERA
# ---------------------------
TOKENIZER_NAME = "openai-community/gpt2"   # 100% open source
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)

report = {}

def count_tokens_from_dataframe(df, dataset_name, chunk_size=10000):
    """
    Liczy tokeny przetwarzając DataFrame w chunkach, aby uniknąć przepełnienia pamięci
    """
    total_tokens = 0
    num_chunks = (len(df) + chunk_size - 1) // chunk_size
    
    print(f"[INFO] {dataset_name}: Przetwarzanie {len(df)} wierszy w {num_chunks} chunkach...")
    
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        text_data = chunk.to_json(orient="records", lines=True)
        tokens = len(tokenizer.encode(text_data))
        total_tokens += tokens
        
        if (i // chunk_size + 1) % 10 == 0:  # Progress co 10 chunków
            print(f"  ... przetworzono {i + len(chunk)}/{len(df)} wierszy")
    
    report[dataset_name] = {
        "rows": len(df),
        "columns": len(df.columns),
        "total_tokens": int(total_tokens)
    }
    print(f"[OK] {dataset_name}: {total_tokens} tokenów")
    return total_tokens

# ----------------------------------------------------------
# 1. Netflix (Kaggle) – wymaga ręcznego pobrania
# ----------------------------------------------------------
def load_netflix_local(path="netflix_titles.csv"):
    if not os.path.exists(path):
        print(f"[WARN] {path} nie istnieje – pobierz z Kaggle!")
        return None
    df = pd.read_csv(path)
    return count_tokens_from_dataframe(df, "Kaggle_Netflix")

# ----------------------------------------------------------
# 2. Wine Quality – UCI
# ----------------------------------------------------------
def load_wine_quality():
    red_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    white_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv"
    df_red = pd.read_csv(red_url, sep=";")
    df_white = pd.read_csv(white_url, sep=";")
    df = pd.concat([df_red, df_white], ignore_index=True)
    return count_tokens_from_dataframe(df, "Wine_Quality")

# ----------------------------------------------------------
# 3. World Bank WDI (LOCAL FOLDER) - Z LIMITAMI
# ----------------------------------------------------------
def load_world_bank_wdi(max_rows_per_file=100000):
    """
    Ładuje pliki WDI z limitem wierszy, aby uniknąć crashu
    max_rows_per_file: maksymalna liczba wierszy do przetworzenia z każdego pliku
    """
    wdi_folder = "wdi_data"
    
    if not os.path.exists(wdi_folder):
        print(f"[ERROR] Folder {wdi_folder} nie istnieje!")
        return None
    
    # Znajdź wszystkie pliki CSV w folderze
    csv_files = glob.glob(os.path.join(wdi_folder, "*.csv"))
    
    if not csv_files:
        print(f"[ERROR] Brak plików CSV w folderze {wdi_folder}!")
        return None
    
    print(f"[INFO] Znaleziono {len(csv_files)} plików CSV w {wdi_folder}")
    
    total_tokens = 0
    
    # Przetwórz każdy plik CSV osobno
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        print(f"\n[INFO] Ładowanie {filename}...")
        
        try:
            # Najpierw sprawdź rozmiar pliku
            file_size_mb = os.path.getsize(csv_file) / (1024 * 1024)
            print(f"  Rozmiar pliku: {file_size_mb:.2f} MB")
            
            # Wczytaj z limitem wierszy dla dużych plików
            if file_size_mb > 50:  # Jeśli plik > 50MB
                print(f"  [WARN] Duży plik! Ograniczam do {max_rows_per_file} wierszy")
                df = pd.read_csv(csv_file, nrows=max_rows_per_file, low_memory=False)
            else:
                df = pd.read_csv(csv_file, low_memory=False)
            
            print(f"  Załadowano {len(df)} wierszy, {len(df.columns)} kolumn")
            
            dataset_name = f"WorldBank_WDI_{filename.replace('.csv', '')}"
            tokens = count_tokens_from_dataframe(df, dataset_name, chunk_size=5000)
            total_tokens += tokens
            
            # Zwolnij pamięć
            del df
            
        except Exception as e:
            print(f"[ERROR] Nie udało się załadować {filename}: {e}")
            continue
    
    print(f"\n[INFO] Łącznie tokenów z WDI: {total_tokens}")
    return total_tokens

# ----------------------------------------------------------
# 4. Titanic – z różnych źródeł
# ----------------------------------------------------------
def load_titanic():
    """
    Próbuje załadować dataset Titanic z różnych źródeł
    """
    print("\n[INFO] Próba załadowania datasetu Titanic...")
    
    # Metoda 1: Z Seaborn (najszybsza i najpewniejsza)
    try:
        import seaborn as sns
        print("[INFO] Ładowanie Titanica z seaborn...")
        df = sns.load_dataset('titanic')
        return count_tokens_from_dataframe(df, "Titanic_Seaborn")
    except Exception as e:
        print(f"[WARN] Seaborn nie zadziałał: {e}")
    
    # Metoda 2: Bezpośrednio z GitHub
    try:
        print("[INFO] Ładowanie Titanica z GitHub...")
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        df = pd.read_csv(url)
        return count_tokens_from_dataframe(df, "Titanic_GitHub")
    except Exception as e:
        print(f"[WARN] GitHub nie zadziałał: {e}")
    
    # Metoda 3: Z Hugging Face (alternatywny dataset)
    try:
        print("[INFO] Ładowanie Titanica z Hugging Face...")
        ds = load_dataset("mstz/titanic", split="train")
        df = ds.to_pandas()
        return count_tokens_from_dataframe(df, "Titanic_HF")
    except Exception as e:
        print(f"[WARN] Hugging Face nie zadziałał: {e}")
    
    # Metoda 4: Lokalny plik (jeśli istnieje)
    try:
        if os.path.exists("titanic.csv"):
            print("[INFO] Ładowanie Titanica z pliku lokalnego...")
            df = pd.read_csv("titanic.csv")
            return count_tokens_from_dataframe(df, "Titanic_Local")
    except Exception as e:
        print(f"[WARN] Plik lokalny nie zadziałał: {e}")
    
    print("[ERROR] Nie udało się załadować datasetu Titanic z żadnego źródła!")
    return None

# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------
if __name__ == "__main__":
    print("\n=== Liczenie tokenów ===\n")
    
    # Możesz wyłączyć niektóre datasety dla testów
    load_netflix_local()
    load_wine_quality()
    
    # WDI z limitem 100k wierszy na plik (możesz zwiększyć jeśli potrzebujesz)
    load_world_bank_wdi(max_rows_per_file=100000)
    load_titanic()
    
    with open("token_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    
    print("\n" + "="*50)
    print("TOKENIZACJA ZAKOŃCZONA – zapisano token_report.json")
    print("="*50)
    
    # Pokaż podsumowanie
    print("\nPODSUMOWANIE:")
    total_all = 0
    for name, data in report.items():
        print(f"  {name}: {data['total_tokens']:,} tokenów ({data['rows']:,} wierszy)")
        total_all += data['total_tokens']
    print(f"\nŁĄCZNIE: {total_all:,} tokenów")