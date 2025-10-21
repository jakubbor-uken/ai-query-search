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



# Wykonywanie programu (21-10-2025):
```
Ścieżka do źródła programu jest ustalana w zmiennej środowiskowej 
`AI_SEARCH_PATH`
bazowo jako ścieżka wykonania skryptu + "/api_keys.json"

przykład wykonania skryptu:
python3 src/main.py "Przywitaj się"

```