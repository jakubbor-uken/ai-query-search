# ai-query-search
Projekt inżynierski 2025/2026 - Aplikacja ustalająca priorytety kategorii danych w zależności od rodzaju zapytania/kwerendy z pomocą AI


# Testowanie API (20-10-2025):
```
#tworzenie środowiska wirtualnego
python3 -m venv .

source bin/activate

#potrzebne pakiety
pip install openai


#wykonaj skrypt testowy
python3 utilities/api-testing.py
```



# Wykonywanie programu (19-11-2025):
```
Parametry wykonania programu są ustalane w pliku
src/main.py

przykład wykonania skryptu:
python3 src/main.py

Rezultat zapisywany jest do konsoli, jak również pliku:
output.log
```


# Bazy danych użyte do przybliżania kosztorysów:

##  Część baz danych należy pobrać i umieścić w folderze przed wykonaniem:
### `https://datacatalogfiles.worldbank.org/ddh-published/0037712/DR0095335/WDI_CSV_10_08.zip` - `utilities/wdi_data/...`
###  `https://www.kaggle.com/datasets/shivamb/netflix-shows` - `utilities/netflix_titles.csv`

### Pozostałe bazy danych są pobierane przez API za pomocą skryptu
`/utilities/db_tokenizer.py`