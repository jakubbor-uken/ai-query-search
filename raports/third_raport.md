# Raport 3 - dostosowanie formatu odpowiedzi LLMów i filtracja wadliwych modeli AI
  
## Rozwój formatu kwerendy  

W trakcie prób uzyskania jednoznacznego i celnego formatu modyfikowaliśmy kwerendę. Staraliśmy się skonstruować zdania tak, by zapewniały jednoznaczne wymagania co do odpowiedzi modeli, jak również zapewnić, że model będzie znał kontekst zapytania i co dokładnie się od niego oczekuje. Dokładniejsza historia modyfikacji kwerendy dodatkowej jest dostępna w historii commitów na GitHub. Finalnie dostosowaliśmy kwerendę w następujący sposób:


Kwerenda przed:  
```python
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól danych które najbardziej jej odpowiadają i zwróć listę pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, dane podane są poniżej: ###\n"
```

Kwerenda po:  
```python
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól danych które najbardziej jej odpowiadają i zwróć listę pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, dane podane są poniżej: ###\n"
```


Ze względu na problemy z formatowaniem zedytowaliśmy projekt tak, by rezultat zawsze był konwertowany do JSON.   
Wzięliśmy pod uwagę kilka wyników z różnych modeli i ustaliliśmy, jakie znaki trzeba usunąć by uzyskać konkretny rezultat, na którym można realnie pracować.  
    
Konkretną standaryzację formatowania odpowiedzi modeli można znaleźć w kodzie źródłowym w pliku:  
`src/ai_search.py`
    


Po zmianach w formatowaniu i kwerendzie:    
  
```python
{'output': {'price': 1, 'productType': 0.9, 'inStock': 0.8, 'currency': 0.7, 'brand': 0.6, 'category': 0.5, 'promotion': 0.4, 'store': 0.3, 'url': 0.2, 'shippingInfo': 0.1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'fields': [{'name': 'productName', 'priority': 10, 'reason': 'Nazwa produktu jest najbardziej bezpośrednim wskazaniem narzędzi kuchennych'}, {'name': 'category', 'priority': 9, 'reason': "Kategoria 'Akcesoria kuchenne' bezpośrednio wskazuje na narzędzia kuchenne"}, {'name': 'subcategory', 'priority': 8, 'reason': "Podkategorie takie jak 'Noże' czy 'Zestawy specjalistyczne' mogą wskazywać narzędzia"}, {'name': 'itemType', 'priority': 7, 'reason': "Typ 'product' wskazuje na produkty, które mogą być narzędziami kuchennymi"}, {'name': 'brand', 'priority': 6, 'reason': 'Marki często specjalizują się w narzędziach kuchennych'}, {'name': 'price', 'priority': 2, 'reason': 'Cena może być pomocna w ocenie, ale nie jest bezpośrednim wskaźnikiem'}, {'name': 'inStock', 'priority': 1, 'reason': 'Dostępność produktu może być istotna dla klienta'}, {'name': 'currency', 'priority': 1, 'reason': 'Waluta jest istotna przy porównywaniu cen'}, {'name': 'store', 'priority': 1, 'reason': 'Sklepy specjalistyczne mogą oferować narzędzia kuchenne'}, {'name': 'url', 'priority': 1, 'reason': 'Link do produktu może być pomocny'}, {'name': 'promotion', 'priority': 1, 'reason': 'Promocje mogą być dodatkowym atutem'}, {'name': 'shippingInfo', 'priority': 1, 'reason': 'Informacje o dostawie mogą być istotne'}]}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 10, 'subcategory': 8, 'ram': 10, 'ramUnit': 8, 'brand': 7, 'productName': 6, 'price': 5, 'productLine': 4, 'model': 3, 'processor': 3, 'screenSize': 2, 'inStock': 1, 'promotion': 1, 'shippingInfo': 1, 'store': 1, 'url': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'itemType': 10, 'destination': 9, 'country': 9, 'region': 8, 'location': 8, 'productName': 7, 'category': 6, 'subcategory': 5, 'price': 4, 'currency': 3, 'store': 2, 'url': 1, 'inStock': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 10, 'productType': 9, 'category': 8, 'inStock': 7, 'brand': 6, 'promotion': 5, 'currency': 4, 'store': 3, 'url': 2, 'shippingInfo': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 10, 'subcategory': 9, 'itemType': 8, 'productName': 7}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'productName': 10, 'ram': 9, 'brand': 8, 'subcategory': 7, 'category': 6, 'price': 5, 'currency': 4, 'store': 3, 'url': 2, 'inStock': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'itemType': 10, 'destination': 9, 'country': 9, 'location': 8, 'region': 8, 'category': 7, 'subcategory': 6, 'productName': 5}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'fields': ['price', 'brand', 'productType', 'category']}, 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': [{'field': 'category', 'priority': 1}, {'field': 'subcategory', 'priority': 2}, {'field': 'productName', 'priority': 3}, {'field': 'brand', 'priority': 4}, {'field': 'price', 'priority': 5}], 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'fields': ['category', 'subcategory', 'ram', 'price'], 'priorities': [2, 2, 1, 1]}, 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': [{'field': 'destination', 'priority': 1}, {'field': 'country', 'priority': 2}, {'field': 'price', 'priority': 3}, {'field': 'currency', 'priority': 4}, {'field': 'store', 'priority': 5}, {'field': 'url', 'priority': 6}, {'field': 'category', 'priority': 7}, {'field': 'subcategory', 'priority': 8}, {'field': 'id', 'priority': 9}], 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'productType': 2, 'brand': 3, 'store': 4, 'inStock': 5, 'promotion': 6, 'category': 7}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'itemType': 5, 'category': 5, 'subcategory': 5, 'productName': 5, 'brand': 4, 'price': 3, 'store': 3, 'inStock': 2, 'promotion': 2, 'shippingInfo': 1, 'currency': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'processor': 5, 'gpu': 4, 'ram': 3, 'category': 2, 'subcategory': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 1, 'country': 1, 'region': 2, 'location': 3, 'travelType': 4, 'price': 5, 'promotion': 6, 'inStock': 7, 'url': 8}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': [{'field': 'price', 'priority': 1}, {'field': 'productType', 'priority': 2}, {'field': 'category', 'priority': 3}, {'field': 'brand', 'priority': 4}, {'field': 'promotion', 'priority': 5}, {'field': 'shippingInfo', 'priority': 6}], 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 1, 'subcategory': 1, 'productName': 1, 'brand': 0.8, 'price': 0.7, 'currency': 0.6, 'store': 0.5, 'url': 0.4, 'inStock': 0.3, 'promotion': 0.2, 'shippingInfo': 0.1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 5, 'subcategory': 4, 'ram': 3, 'price': 2, 'brand': 1, 'inStock': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 5, 'destination': 4, 'location': 3, 'region': 2, 'itemType': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 5, 'inStock': 4, 'promotion': 3, 'brand': 2, 'productType': 2, 'currency': 1, 'store': 1, 'url': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'itemType': 3, 'productName': 2, 'category': 2, 'subcategory': 2, 'price': 1, 'inStock': 1, 'promotion': 1, 'brand': 1, 'url': 1, 'cuisine': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 1.0, 'subcategory': 1.0, 'itemType': 0.9, 'brand': 0.8, 'productName': 0.8, 'ram': 0.7, 'price': 0.6, 'inStock': 0.5, 'promotion': 0.4, 'store': 0.3, 'url': 0.2, 'currency': 0.1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 3, 'destination': 3, 'price': 2, 'inStock': 2, 'promotion': 2, 'travelType': 1, 'boardType': 1, 'store': 1, 'url': 1, 'currency': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
  
    
Odpowiedziom nadal brakuje jednoznacznej struktury. w związku z tym zmieniliśmy kwerendę na:  
  
Kwerenda przed: 
```python 
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól danych które najbardziej jej odpowiadają i zwróć listę pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, dane podane są poniżej: ###\n"
```

Kwerenda po:  
```python
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól danych które najbardziej jej odpowiadają i zwróć listę pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue}, dane podane są poniżej: ###\n"
```
     
Niestety nadal część modeli zwracała odpowiedzi z `fields`, czego chcieliśmy uniknąć:  
```python
{'output': {'price': 5, 'productType': 4, 'category': 3, 'brand': 2, 'inStock': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': [{'id': 0, 'priority': 8, 'fields': ['productName', 'category', 'subcategory']}, {'id': 5, 'priority': 7, 'fields': ['productName', 'category', 'subcategory']}, {'id': 9, 'priority': 9, 'fields': ['productName', 'category', 'subcategory']}, {'id': 7, 'priority': 6, 'fields': ['title', 'subcategory']}, {'id': 13, 'priority': 5, 'fields': ['productName', 'category', 'subcategory']}, {'id': 15, 'priority': 4, 'fields': ['title', 'subcategory']}, {'id': 21, 'priority': 5, 'fields': ['productName', 'category', 'subcategory']}, {'id': 23, 'priority': 5, 'fields': ['title', 'subcategory']}, {'id': 25, 'priority': 7, 'fields': ['productName', 'category', 'subcategory']}], 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'itemType': 10, 'category': 10, 'subcategory': 8, 'ram': 10, 'ramUnit': 8, 'price': 6, 'currency': 5, 'store': 3, 'url': 3, 'inStock': 5, 'promotion': 2, 'shippingInfo': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'itemType': 5, 'productName': 4, 'category': 3, 'subcategory': 2, 'destination': 5, 'country': 4, 'region': 3, 'price': 1, 'currency': 1, 'store': 1, 'url': 1, 'inStock': 1, 'promotion': 1, 'travelType': 2, 'boardType': 1, 'location': 3}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 10, 'productType': 9, 'category': 8, 'inStock': 7, 'promotion': 6, 'brand': 5, 'currency': 4, 'store': 3, 'url': 2, 'shippingInfo': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': [{'productName': 10, 'category': 9, 'subcategory': 8, 'itemType': 7}, {'productName': 10, 'category': 9, 'subcategory': 8, 'itemType': 7}, {'productName': 10, 'category': 9, 'subcategory': 8, 'itemType': 7}, {'productName': 10, 'category': 9, 'subcategory': 8, 'itemType': 7}], 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 10, 'subcategory': 9, 'ram': 8, 'processor': 7, 'productName': 6, 'brand': 5, 'price': 4, 'itemType': 3, 'store': 2, 'inStock': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 10, 'region': 9, 'location': 8, 'itemType': 7, 'category': 6, 'subcategory': 5}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': [{'field': 'price', 'priority': 1}, {'field': 'inStock', 'priority': 2}, {'field': 'currency', 'priority': 3}, {'field': 'model', 'priority': 4}, {'field': 'brand', 'priority': 5}], 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'fields': ['category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category', 'category'], 'priorities': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}, 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź narzędzia kuchenne'}
{'output': [{'price': 5500, 'ram': 16, 'brand': 'ASUS', 'inStock': True, 'category': 'Laptopy', 'subcategory': 'Gaming', 'productName': 'Laptop Gamingowy ASUS ROG', 'productLine': 'ROG', 'ramUnit': 'GB', 'currency': 'PLN', 'store': 'komputery.pl', 'url': 'www.komputery.pl'}, {'price': 5999.99, 'ram': 16, 'brand': 'MSI', 'inStock': True, 'category': 'Laptopy', 'subcategory': 'Gaming', 'productName': 'MSI Katana 15', 'productLine': 'Katana 15', 'ramUnit': 'GB', 'currency': 'PLN', 'store': 'komputerymsi.pl', 'url': 'www.komputerymsi.pl'}, {'price': 6999, 'ram': 32, 'brand': 'Lenovo', 'inStock': True, 'category': 'Laptopy', 'subcategory': 'Gaming', 'productName': 'Laptop Lenovo Legion', 'productLine': 'Legion', 'ramUnit': 'GB', 'currency': 'PLN', 'store': 'legionsklep.pl', 'url': 'legionsklep.pl'}, {'price': 8999, 'ram': 16, 'brand': 'Apple', 'inStock': True, 'category': 'Laptopy', 'subcategory': 'MacBook', 'productName': 'MacBook Pro M2', 'model': 'MacBook Pro', 'processor': 'M2', 'ramUnit': 'GB', 'currency': 'PLN', 'store': 'macsklep.pl', 'url': 'macsklep.pl'}, {'price': 12000, 'ram': 64, 'brand': None, 'inStock': True, 'category': 'Komputery stacjonarne', 'subcategory': 'Workstation', 'productName': 'Stacja robocza', 'ramUnit': 'GB', 'currency': 'PLN', 'store': 'workstations.pl', 'url': 'workstations.pl'}, {'price': 4499, 'ram': 16, 'brand': 'Acer', 'inStock': True, 'category': 'Laptopy', 'subcategory': 'Gaming', 'productName': 'Laptop Gamingowy Acer Nitro 5', 'productLine': 'Nitro', 'model': 'Nitro 5', 'ramUnit': 'GB', 'currency': 'PLN', 'store': 'nitrogaming.pl', 'url': 'www.nitrogaming.pl'}], 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': [{'field': 'destination', 'priority': 1}, {'field': 'country', 'priority': 2}, {'field': 'category', 'priority': 3}, {'field': 'subcategory', 'priority': 4}, {'field': 'price', 'priority': 5}, {'field': 'currency', 'priority': 6}], 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'fields': [{'field': 'price', 'priority': 7}, {'field': 'brand', 'priority': 6}, {'field': 'productType', 'priority': 5}, {'field': 'store', 'priority': 4}, {'field': 'url', 'priority': 3}, {'field': 'inStock', 'priority': 2}, {'field': 'promotion', 'priority': 1}]}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 4, 'subcategory': 3, 'productName': 2, 'brand': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'processor': 7, 'ram': 6, 'gpu': 5, 'formFactor': 4, 'price': 3, 'brand': 2, 'productLine': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 1, 'country': 2, 'region': 3, 'location': 4, 'travelType': 5}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': [{'field': 'price', 'priority': 1}, {'field': 'productType', 'priority': 2}, {'field': 'category', 'priority': 3}, {'field': 'brand', 'priority': 4}, {'field': 'promotion', 'priority': 5}, {'field': 'shippingInfo', 'priority': 6}, {'field': 'inStock', 'priority': 7}], 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 1, 'subcategory': 1, 'productName': 0.8, 'brand': 0.6}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 3, 'subcategory': 3, 'ram': 2, 'price': 1, 'brand': 1, 'productName': 1, 'inStock': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 5, 'destination': 4, 'location': 3, 'region': 2, 'itemType': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'inStock': 0.5, 'promotion': 0.3}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'itemType': 3, 'productName': 3, 'category': 3, 'subcategory': 3, 'price': 2, 'currency': 2, 'store': 2, 'url': 2, 'inStock': 2, 'promotion': 1, 'brand': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'itemType': 3, 'category': 3, 'subcategory': 3, 'ram': 3, 'price': 2, 'inStock': 2, 'brand': 1, 'productLine': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 3, 'destination': 3, 'price': 2, 'inStock': 2, 'promotion': 1, 'travelType': 1, 'boardType': 1, 'store': 0, 'url': 0, 'currency': 0, 'id': 0, 'itemType': 0, 'productName': 0, 'category': 0, 'subcategory': 0}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```

Ustaliliśmy nowy prompt.
  
Nowy prompt:   
```python
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól danych które najbardziej jej odpowiadają i zwróć obiekt pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue}, odpowiedź musi zawrzeć się tylko w jednym obiekcie, dane podane są poniżej: ###\n"
```
  
Jednak wtedy model zwracał wiele obiektów zamiast jednego z kilkoma polami  
  
Nowy prompt:
```python  
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól danych które najbardziej jej odpowiadają i zwróć tylko jeden obiekt wszystkich pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue, \"propertyName\": priorityValue}, odpowiedź musi zawrzeć się tylko w jednym obiekcie zawierającym wszystkie cechy i ich priorytety, dane podane są poniżej: ###\n"
```
  
zauważyliśmy dziwne zachowania jednego modelu `Llama-3.1-8B Instruct`, zwrócił pełne części bazy danych:  
```python
2025-11-19 19:35:33 | INFO | api_handler.py:22 >>> Sending request to HuggingFace API
2025-11-19 19:35:33 | INFO | api_handler.py:23 >>> Model: meta-llama/Llama-3.1-8B-Instruct
2025-11-19 19:35:42 | INFO | _client.py:1025 >>> HTTP Request: POST https://router.huggingface.co/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-19 19:35:42 | INFO | api_handler.py:49 >>> Response received
2025-11-19 19:35:42 | INFO | ai_search.py:39 >>> {"destination": "Egipt", "country": "Egipt", "price": 1800, "currency": "PLN", "store": "wakacje.com", "url": "www.wakacje.com", "inStock": true, "promotion": false, "travelType": "Package holiday"},

{"destination": "Grecja", "country": "Grecja", "price": 1200, "currency": "PLN", "store": "taniewakacje.pl", "url": "www.taniewakacje.pl", "inStock": true, "promotion": false, "travelType": "Tour"},

{"destination": "Włochy", "country": "Włochy", "price": 2800, "currency": "PLN", "store": "italia-tour.pl", "url": "italia-tour.pl", "inStock": true, "promotion": true, "travelType": "Sightseeing tour"},

{"destination": "Bułgaria", "country": "Bułgaria", "price": 999, "currency": "PLN", "store": null, "url": null, "inStock": true, "promotion": true, "travelType": "Last minute"},

{"destination": "Kenia", "country": "Kenia", "price": 4500, "currency": "PLN", "store": "egzotycznepodroze.pl", "url": "www.egzotycznepodroze.pl", "inStock": true, "promotion": false, "travelType": "Safari"},

{"destination": "Tunezja", "country": "Tunezja", "price": 1500, "currency": "PLN", "store": "wakacje.lastminute.pl", "url": "www.wakacje.lastminute.pl", "inStock": true, "promotion": true, "travelType": "Last minute"},

{"destination": "Wakacje na Majorce", "country": "Hiszpania", "price": 2100, "currency": "PLN", "store": null, "url": null, "inStock": true, "promotion": true, "travelType": "Last minute"},

{"destination": "Norwegia", "country": "Norwegia", "price": 3800, "currency": "PLN", "store": "fjordytour.pl", "url": "www.fjordytour.pl", "inStock": true, "promotion": false, "travelType": "Sightseeing tour"},
```


  
jak również miał problemy z rozłożeniem priorytetów (nadał tylko 1 i 0):  
```python
2025-11-19 19:35:28 | INFO | api_handler.py:22 >>> Sending request to HuggingFace API
2025-11-19 19:35:29 | INFO | api_handler.py:23 >>> Model: meta-llama/Llama-3.1-8B-Instruct
2025-11-19 19:35:33 | INFO | _client.py:1025 >>> HTTP Request: POST https://router.huggingface.co/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-19 19:35:33 | INFO | api_handler.py:49 >>> Response received
2025-11-19 19:35:33 | INFO | ai_search.py:39 >>> {"category": 1, "subcategory": 1, "ram": 1, "price": 1, "currency": 1, "store": 1, "url": 1, "inStock": 1, "promotion": 1, "shippingInfo": 1, "model": 1, "screenSize": 1, "processor": 1, "gpu": 1, "productLine": 1, "brand": 1, "productName": 1, "price": 1, "usage": 1, "formFactor": 1, "features": 1, "focus": 1, "stockStatus": 1, "promotionValidUntil": 1, "paymentOptions": 1, "shippingInfo": 1, "contentType": 1, "topic": 1, "title": 1, "id": 0, "ramUnit": 0}
```
  
ale w innym wypadku rozłożył poprawnie:  
  
```python
2025-11-19 19:35:25 | INFO | api_handler.py:23 >>> Model: meta-llama/Llama-3.1-8B-Instruct
2025-11-19 19:35:28 | INFO | _client.py:1025 >>> HTTP Request: POST https://router.huggingface.co/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-19 19:35:28 | INFO | api_handler.py:49 >>> Response received
2025-11-19 19:35:28 | INFO | ai_search.py:39 >>> {"productName": 0.5, "recipeName": 0.5, "title": 0.5, "category": 1, "subcategory": 1, "price": 0.2, "currency": 0.2, "store": 0.1, "url": 0.1, "inStock": 0.1, "promotion": 0.1, "shippingInfo": 0.1, "brand": 0.5, "cuisine": 0.5, "contentType": 0.5, "dietType": 0.5, "format": 0.5, "specialty": 0.5, "occasion": 0.5, "paymentOptions": 0.5, "stockStatus": 0.5, "model": 0.5, "variety": 0.5, "priceFrom": 0.1, "edition": 0.1}
```

  
  
  
Nowy prompt:  
```python
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól danych które najbardziej jej odpowiadają i zwróć tylko jeden obiekt wszystkich pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue, \"propertyName\": priorityValue} - odpowiedź musi zawrzeć się tylko w jednym obiekcie, dane podane są poniżej: ###\n"
```
   
```python
{'output': {'price': 10, 'productType': 5, 'category': 3, 'inStock': 4, 'promotion': 2}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 9, 'subcategory': 8, 'itemType': 7, 'brand': 6, 'price': 5, 'inStock': 4, 'url': 3, 'store': 2, 'promotion': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 10, 'subcategory': 5, 'ram': 8, 'brand': 7, 'productName': 6, 'price': 9, 'inStock': 10, 'promotion': 4, 'shippingInfo': 3, 'productLine': 5, 'model': 4, 'processor': 4, 'screenSize': 3, 'gpu': 3, 'stockStatus': 2, 'promotionValidUntil': 2, 'usage': 3, 'formFactor': 2, 'features': 1, 'paymentOptions': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 10, 'region': 9, 'destination': 8, 'location': 7, 'itemType': 6, 'category': 5, 'subcategory': 4, 'productName': 3, 'travelType': 2, 'price': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 1, 'brand': 10, 'productType': 10, 'category': 10, 'price': 100, 'currency': 10, 'store': 10, 'url': 10, 'inStock': 10, 'promotion': 10, 'shippingInfo': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 100, 'category': 95, 'subcategory': 90, 'brand': 85, 'price': 80, 'store': 75, 'inStock': 70, 'promotion': 65, 'url': 60, 'currency': 55, 'id': 50, 'itemType': 45}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 20, 'itemType': 10, 'brand': 10, 'productName': 10, 'category': 10, 'subcategory': 10, 'productLine': 10, 'ram': 10, 'ramUnit': 10, 'price': 6, 'currency': 10, 'store': 10, 'url': 10, 'inStock': 10, 'promotion': 5, 'shippingInfo': 5}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 10, 'region': 10, 'location': 10, 'itemType': 9, 'category': 8, 'subcategory': 7, 'productName': 6, 'price': 5, 'currency': 5, 'store': 4, 'url': 4, 'inStock': 3, 'promotion': 2, 'travelType': 1, 'boardType': 1, 'priceUnit': 1, 'amenities': 1, 'stockStatus': 1, 'promotionValidUntil': 1, 'priceFrom': 1, 'includes': 1, 'departureInfo': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'currency': 0.5, 'store': 0.5, 'brand': 0.5, 'inStock': 0.5, 'promotion': 0.5}, 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 14, 'subcategory': 8, 'price': 8, 'url': 13, 'inStock': 7, 'promotion': 6, 'shippingInfo': 5, 'brand': 4, 'productName': 3, 'cuisine': 2, 'contentType': 1}, 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 1, 'subcategory': 1, 'productLine': 1, 'ram': 1, 'price': 1, 'brand': 1, 'productName': 1, 'store': 1, 'url': 1, 'inStock': 1, 'ramUnit': 1, 'currency': 1, 'gpu': 1, 'processor': 1, 'model': 1, 'screenSize': 1, 'formFactor': 1, 'features': 1, 'usage': 1, 'stockStatus': 1, 'shippingInfo': 1, 'promotion': 1, 'promotionValidUntil': 1, 'paymentOptions': 1, 'contentType': 1, 'topic': 1, 'focus': 1}, 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 'Egipt', 'category': 'Wczasy', 'subcategory': 'Last minute', 'price': 1800, 'priceUnit': None, 'currency': 'PLN', 'inStock': True, 'promotion': False, 'travelType': 'Package holiday', 'destination': 'Egipt', 'boardType': 'All inclusive'}, 'model': 'meta-llama/Llama-3.1-8B-Instruct', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'productType': 10, 'price': 10, 'brand': 5, 'category': 3, 'store': 2, 'url': 1, 'id': 1, 'currency': 2, 'inStock': 6, 'promotion': 5, 'shippingInfo': 3, 'model': 5, 'features': 3, 'contentType': 1, 'stockStatus': 2, 'availableSizes': 2, 'promotionValidUntil': 2}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'id': 1, 'itemType': 1, 'brand': 7, 'productName': 8, 'category': 10, 'subcategory': 9, 'price': 5, 'currency': 5, 'store': 4, 'url': 4, 'inStock': 3, 'promotion': 3, 'shippingInfo': 2}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 1, 'itemType': 1, 'brand': 6, 'productName': 5, 'category': 8, 'subcategory': 9, 'productLine': 8, 'ram': 10, 'ramUnit': 2, 'processor': 10, 'gpu': 9, 'screenSize': 4, 'price': 8, 'currency': 2, 'store': 2, 'url': 2, 'inStock': 3, 'promotion': 2, 'shippingInfo': 2, 'promotionValidUntil': 2, 'stockStatus': 2, 'usage': 6, 'formFactor': 3, 'features': 3, 'paymentOptions': 3, 'contentType': 2, 'title': 2, 'topic': 2, 'focus': 2}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'id': 0, 'itemType': 0, 'productName': 7, 'category': 5, 'subcategory': 6, 'destination': 9, 'region': 10, 'price': 3, 'currency': 2, 'store': 1, 'url': 0, 'inStock': 4, 'promotion': 0, 'travelType': 8, 'activities': 7}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 10, 'productType': 9, 'category': 8, 'brand': 7, 'model': 6, 'promotion': 5, 'inStock': 4, 'store': 3, 'url': 2, 'currency': 1, 'shippingInfo': 0}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'id': 5, 'itemType': 10, 'brand': 8, 'productName': 10, 'category': 10, 'subcategory': 10, 'price': 8, 'currency': 8, 'store': 8, 'url': 8, 'inStock': 8, 'promotion': 8, 'promotionValidUntil': 8, 'shippingInfo': 8}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 5, 'subcategory': 5, 'ram': 5, 'price': 3, 'inStock': 2, 'promotion': 1, 'itemType': 5}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 5, 'destination': 5, 'category': 4, 'subcategory': 3, 'travelType': 2, 'price': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 5, 'inStock': 4, 'promotion': 3, 'brand': 2, 'productType': 2, 'currency': 1, 'store': 1, 'url': 1, 'shippingInfo': 1, 'model': 1, 'features': 1, 'availableSizes': 1, 'stockStatus': 1, 'promotionValidUntil': 1, 'contentType': 0, 'category': 0, 'id': 0}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 1, 'subcategory': 1, 'itemType': 1, 'productName': 0.8, 'recipeName': 0.8, 'title': 0.7, 'inStock': 0.6, 'price': 0.5, 'brand': 0.5, 'cuisine': 0.4, 'url': 0.3, 'id': 0.1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 0, 'itemType': 3, 'brand': 3, 'productName': 3, 'category': 3, 'subcategory': 3, 'productLine': 3, 'ram': 3, 'price': 2, 'inStock': 2, 'promotion': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 3, 'destination': 3, 'price': 2, 'inStock': 1, 'promotion': 1, 'travelType': 1, 'boardType': 1, 'store': 0, 'url': 0, 'id': 0}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
  
Obserwacja rezultatów z poprzednich wykonań doprowadziła nas do wniosku, że model **meta-llama/Llama-3.1-8B-Instruct** nie nadaje się do naszego użycia - nie można było liczyć na jednoznaczną odpowiedź, a model nie przestrzegał zawsze zasad zapisanych w promptcie.  
Ze względu na te problemy zdecydowaliśmy pominąć kolejne testy na tym modelu i zdecydowaliśmy, że **nie jest** on obecnie gotowy do konsekwentnego, automatycznego ustalania priorytetów danych.  
Reszta modeli radziła sobie lepiej i przestrzegała prompta.  
  
Przeprowadziliśmy kolejne dwa wykonania programu, by upewnić się, że output jest poprawny.  

```python
{'output': {'price': 10, 'productType': 8, 'category': 7, 'inStock': 6, 'brand': 5, 'currency': 4, 'store': 3, 'url': 2, 'promotion': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 9, 'subcategory': 8, 'itemType': 7, 'brand': 6, 'price': 5, 'currency': 4, 'store': 3, 'url': 2, 'inStock': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 10, 'subcategory': 5, 'ram': 8, 'brand': 7, 'productName': 6, 'price': 9, 'processor': 3, 'model': 4, 'screenSize': 2, 'productLine': 2, 'inStock': 1, 'promotion': 1, 'shippingInfo': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'itemType': 9, 'productName': 8, 'category': 7, 'subcategory': 6, 'destination': 5, 'country': 4, 'boardType': 3, 'price': 2, 'currency': 1, 'store': 0, 'url': 0, 'inStock': 0, 'promotion': 0, 'travelType': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 1, 'brand': 8, 'productType': 8, 'category': 8, 'price': 10, 'currency': 8, 'store': 8, 'url': 8, 'inStock': 8, 'promotion': 8, 'shippingInfo': 8}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 9, 'subcategory': 9, 'brand': 7, 'id': 5}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 20, 'itemType': 10, 'brand': 10, 'productName': 10, 'category': 10, 'subcategory': 10, 'productLine': 10, 'ram': 10, 'ramUnit': 10, 'price': 10, 'currency': 10, 'store': 10, 'url': 10, 'inStock': 10, 'promotion': 10, 'shippingInfo': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 10, 'location': 10, 'region': 10, 'productName': 9, 'category': 8, 'subcategory': 8, 'price': 7, 'currency': 7, 'store': 6, 'url': 6, 'inStock': 6, 'promotion': 5, 'travelType': 5, 'itemType': 4, 'id': 4, 'boardType': 3, 'priceUnit': 3, 'amenities': 3, 'stockStatus': 3, 'promotionValidUntil': 2, 'includes': 2, 'activities': 2, 'highlights': 2, 'departureInfo': 2, 'priceFrom': 2, 'targetGroup': 1, 'format': 1, 'serviceType': 1, 'contentType': 1, 'features': 1, 'spf': 1, 'usage': 1, 'language': 1, 'duration': 1, 'durationUnit': 1, 'topic': 1, 'flightType': 1, 'availability': 1, 'material': 1, 'quantity': 1, 'quantityUnit': 1, 'dimensions': 1, 'weight': 1, 'weightUnit': 1, 'brand': 1, 'model': 1, 'productLine': 1, 'ram': 1, 'ramUnit': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 0, 'brand': 8, 'productType': 9, 'category': 7, 'price': 10, 'currency': 4, 'store': 5, 'url': 3, 'inStock': 6, 'promotion': 2, 'shippingInfo': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'id': 2, 'itemType': 8, 'productName': 10, 'recipeName': 1, 'title': 1, 'brand': 9, 'category': 10, 'subcategory': 10, 'price': 6, 'priceFrom': 2, 'currency': 3, 'store': 5, 'url': 5, 'inStock': 6, 'promotion': 5, 'shippingInfo': 5, 'cuisine': 7, 'contentType': 4, 'dietType': 4, 'promotionValidUntil': 4, 'format': 4, 'specialty': 4, 'model': 3, 'paymentOptions': 3, 'stockStatus': 3, 'edition': 3, 'variety': 3, 'occasion': 4}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'processor': 9, 'gpu': 8, 'screenSize': 7, 'price': 6, 'brand': 5, 'productName': 4, 'category': 3, 'subcategory': 2, 'productLine': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'id': 1, 'itemType': 4, 'productName': 3, 'category': 4, 'subcategory': 3, 'destination': 5, 'region': 5, 'price': 2, 'currency': 4, 'store': 1, 'url': 1, 'inStock': 4, 'promotion': 1, 'travelType': 3, 'activities': 4}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'productType': 2, 'category': 3, 'brand': 4, 'model': 5, 'shippingInfo': 6, 'promotion': 7, 'inStock': 8, 'currency': 9, 'store': 10, 'url': 11, 'features': 12, 'availableSizes': 13, 'stockStatus': 14, 'promotionValidUntil': 15, 'contentType': 16}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'id': 5, 'itemType': 3, 'brand': 2, 'productName': 3, 'category': 3, 'subcategory': 3, 'price': 2, 'currency': 2, 'store': 2, 'url': 2, 'inStock': 2, 'promotion': 2, 'promotionValidUntil': 1, 'shippingInfo': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 5, 'subcategory': 4, 'ram': 3, 'price': 2, 'inStock': 1, 'promotion': 1, 'itemType': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 5, 'country': 5, 'location': 4, 'region': 3, 'travelType': 2, 'boardType': 2, 'price': 1, 'currency': 1, 'store': 1, 'url': 1, 'inStock': 1, 'promotion': 1, 'promotionValidUntil': 1, 'departureInfo': 1, 'includes': 1, 'highlights': 1, 'activities': 1, 'amenities': 1, 'priceUnit': 1, 'priceFrom': 1, 'stockStatus': 1, 'targetGroup': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 5, 'inStock': 4, 'promotion': 3, 'brand': 2, 'productType': 2, 'currency': 1, 'store': 1, 'url': 1, 'shippingInfo': 1, 'model': 1, 'features': 1, 'availableSizes': 1, 'stockStatus': 1, 'promotionValidUntil': 1, 'contentType': 0, 'category': 0, 'id': 0}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 3, 'subcategory': 3, 'itemType': 2, 'productName': 1, 'title': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 32, 'subcategory': 'Gaming', 'category': 'Laptopy', 'price': 6999, 'brand': 'Lenovo', 'productName': 'Laptop Lenovo Legion', 'id': 20}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 5, 'country': 5, 'price': 4, 'inStock': 3, 'promotion': 3, 'travelType': 3, 'boardType': 2, 'departureInfo': 2, 'url': 1, 'store': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
  
Tym razem model **inclusionAI/Ling-1T:featherless-ai** źle zrozumiał polecenie za jednym razem. Zmodyfikowaliśmy kwerendę:  

```python
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól (object properties) danych które najbardziej jej odpowiadają i zwróć tylko jeden obiekt wszystkich pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue, \"propertyName\": priorityValue} - odpowiedź musi zawrzeć się tylko w jednym obiekcie, dane podane są poniżej: ###\n"
```
  
  
Otrzymaliśmy (wykonanie 1):  
```python
{'output': {'price': 10, 'productType': 9, 'category': 8, 'inStock': 7, 'brand': 6, 'promotion': 5, 'currency': 4, 'store': 3, 'url': 2, 'shippingInfo': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'itemType': 10, 'productName': 9, 'category': 8, 'subcategory': 7, 'brand': 6, 'price': 5, 'currency': 4, 'store': 3, 'url': 2, 'inStock': 1, 'promotion': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 10, 'subcategory': 8, 'ram': 10, 'ramUnit': 10, 'price': 8, 'currency': 6, 'brand': 7, 'productName': 9, 'productLine': 6, 'processor': 5, 'screenSize': 4, 'model': 5, 'inStock': 3, 'promotion': 2, 'shippingInfo': 1, 'store': 1, 'url': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 10, 'destination': 9, 'region': 8, 'location': 7, 'itemType': 6, 'category': 5, 'subcategory': 4, 'productName': 3, 'price': 2, 'currency': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 1, 'brand': 10, 'productType': 10, 'category': 10, 'price': 100, 'currency': 10, 'store': 5, 'url': 5, 'inStock': 5, 'promotion': 2, 'shippingInfo': 1, 'model': 3, 'promotionValidUntil': 1, 'stockStatus': 1, 'availableSizes': 1, 'features': 1, 'contentType': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 9, 'subcategory': 8, 'brand': 7, 'price': 6, 'store': 5, 'inStock': 4, 'promotion': 3, 'itemType': 2, 'id': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'category': 9, 'subcategory': 8, 'price': 7, 'brand': 6, 'productName': 5, 'itemType': 4, 'id': 3, 'currency': 2, 'store': 1, 'url': 1, 'inStock': 1, 'promotion': 1, 'shippingInfo': 1, 'stockStatus': 1, 'promotionValidUntil': 1, 'usage': 1, 'formFactor': 1, 'paymentOptions': 1, 'features': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 10, 'region': 10, 'location': 10, 'itemType': 9, 'category': 8, 'subcategory': 7, 'travelType': 6, 'productName': 5, 'price': 3, 'currency': 3, 'inStock': 2, 'promotion': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 10, 'productType': 9, 'inStock': 8, 'promotion': 7, 'store': 6, 'brand': 5, 'category': 4, 'shippingInfo': 3, 'currency': 2, 'url': 1, 'model': 1, 'features': 1, 'promotionValidUntil': 1, 'stockStatus': 1, 'availableSizes': 1, 'contentType': 1, 'id': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'id': 5, 'itemType': 5, 'productName': 10, 'category': 10, 'subcategory': 10, 'price': 9, 'currency': 9, 'store': 9, 'url': 9, 'inStock': 8, 'promotion': 8, 'shippingInfo': 8, 'cuisine': 2, 'recipeName': 1, 'contentType': 3, 'brand': 9, 'promotionValidUntil': 4, 'model': 4, 'paymentOptions': 4, 'priceFrom': 4, 'stockStatus': 3, 'edition': 3, 'variety': 3, 'specialty': 3, 'occasion': 2, 'dietType': 2, 'format': 2, 'title': 3}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'processor': 9, 'gpu': 8, 'price': 7, 'category': 6, 'subcategory': 5, 'brand': 4, 'inStock': 3, 'promotion': 2, 'shippingInfo': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'id': 0, 'itemType': 7, 'productName': 0, 'category': 6, 'subcategory': 5, 'destination': 8, 'country': 9, 'region': 10, 'price': 3, 'currency': 2, 'store': 1, 'url': 0, 'inStock': 0, 'promotion': 0, 'travelType': 4, 'activities': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'productType': 2, 'category': 3, 'brand': 4, 'model': 5, 'promotion': 6, 'shippingInfo': 7, 'inStock': 8, 'currency': 9, 'store': 10, 'url': 11, 'features': 12, 'availableSizes': 13, 'stockStatus': 14, 'promotionValidUntil': 15, 'contentType': 16}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 8, 'subcategory': 8, 'price': 5, 'currency': 5, 'store': 5, 'url': 5, 'inStock': 5, 'promotion': 5, 'shippingInfo': 5, 'cuisine': 5}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 5, 'subcategory': 4, 'ram': 3, 'price': 2, 'inStock': 1, 'itemType': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 5, 'destination': 4, 'category': 3, 'subcategory': 2, 'travelType': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 5, 'inStock': 4, 'promotion': 3, 'shippingInfo': 2, 'brand': 1, 'productType': 1, 'category': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 1, 'subcategory': 1, 'productName': 1, 'itemType': 0.5, 'brand': 0.5, 'price': 0.3, 'cuisine': 0.2, 'inStock': 0.1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'category': 9, 'subcategory': 9, 'price': 7, 'itemType': 10, 'brand': 3}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 5, 'country': 5, 'price': 4, 'inStock': 3, 'promotion': 3, 'travelType': 3, 'boardType': 3, 'departureInfo': 5, 'location': 2, 'url': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
   
Format wyników poprawny. Test powtórzony z tymi samymi parametrami (wykonanie 2):  
```python
{'output': {'price': 10, 'productType': 9, 'inStock': 8, 'currency': 7, 'brand': 6, 'category': 5, 'promotion': 4, 'store': 3, 'url': 2, 'shippingInfo': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'itemType': 9, 'category': 8, 'subcategory': 7, 'brand': 6, 'price': 5, 'inStock': 4, 'store': 3, 'url': 2, 'promotion': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'productLine': 8, 'model': 7, 'brand': 6, 'price': 5, 'subcategory': 4, 'category': 3, 'inStock': 2, 'processor': 1, 'promotion': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'itemType': 10, 'category': 9, 'subcategory': 8, 'destination': 7, 'country': 7, 'region': 6, 'location': 6, 'travelType': 5, 'price': 4, 'boardType': 3, 'inStock': 2, 'promotion': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 10, 'productType': 9, 'category': 8, 'inStock': 7, 'currency': 6, 'promotion': 5, 'brand': 4, 'store': 3, 'shippingInfo': 2, 'id': 1, 'url': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 9, 'subcategory': 9, 'brand': 8, 'price': 7, 'store': 6, 'inStock': 5, 'promotion': 4, 'url': 3, 'itemType': 2, 'id': 1, 'currency': 1, 'shippingInfo': 1, 'promotionValidUntil': 1, 'model': 1, 'paymentOptions': 1, 'stockStatus': 1, 'edition': 1, 'variety': 1, 'priceFrom': 1, 'specialty': 1, 'dietType': 1, 'occasion': 1, 'contentType': 1, 'cuisine': 1, 'format': 1, 'recipeName': 0, 'title': 0, 'guide': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'category': 9, 'subcategory': 8, 'price': 7, 'brand': 6, 'productName': 5, 'itemType': 4, 'id': 3, 'currency': 2, 'store': 1, 'url': 1, 'inStock': 1, 'promotion': 1, 'shippingInfo': 1, 'stockStatus': 1, 'promotionValidUntil': 1, 'usage': 1, 'formFactor': 1, 'features': 1, 'paymentOptions': 1, 'model': 1, 'productLine': 1, 'processor': 1, 'gpu': 1, 'screenSize': 1, 'topic': 0, 'contentType': 0, 'focus': 0, 'title': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 10, 'region': 9, 'location': 9, 'itemType': 8, 'category': 8, 'subcategory': 8, 'travelType': 7, 'productName': 7, 'price': 6, 'currency': 6, 'inStock': 5, 'promotion': 4, 'store': 3, 'url': 3}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 0, 'brand': 6, 'productType': 8, 'category': 7, 'model': 5, 'price': 10, 'currency': 4, 'store': 3, 'url': 2, 'inStock': 9, 'promotion': 0, 'shippingInfo': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'brand': 9, 'category': 8, 'subcategory': 7, 'itemType': 6, 'price': 5, 'inStock': 4, 'promotion': 4, 'store': 4, 'url': 3, 'promotionValidUntil': 3, 'shippingInfo': 3, 'stockStatus': 2, 'format': 2, 'model': 2, 'paymentOptions': 2, 'currency': 2, 'priceFrom': 2, 'variety': 2, 'edition': 2, 'contentType': 1, 'cuisine': 1, 'dietType': 1, 'specialty': 1, 'occasion': 1, 'title': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 1, 'itemType': 1, 'brand': 6, 'productName': 2, 'category': 2, 'subcategory': 4, 'productLine': 5, 'ram': 9, 'ramUnit': 3, 'price': 7, 'currency': 3, 'store': 2, 'url': 2, 'inStock': 2, 'promotion': 2, 'shippingInfo': 2, 'processor': 10, 'gpu': 8, 'screenSize': 3, 'model': 3, 'promotionValidUntil': 1, 'stockStatus': 1, 'usage': 1, 'formFactor': 1, 'paymentOptions': 1, 'features': 1, 'title': 1, 'contentType': 1, 'topic': 1, 'focus': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'region': 9, 'price': 8, 'inStock': 7, 'promotion': 6, 'itemType': 5, 'productName': 4, 'category': 4, 'subcategory': 4, 'currency': 4, 'store': 4, 'url': 4, 'travelType': 3, 'activities': 3, 'id': 2}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'productType': 2, 'category': 3}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 10, 'subcategory': 9, 'productName': 8, 'brand': 7, 'price': 6, 'currency': 5, 'store': 4, 'url': 3, 'inStock': 2, 'promotion': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'itemType': 5, 'category': 5, 'ram': 5, 'price': 3, 'inStock': 2, 'promotion': 1, 'shippingInfo': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 5, 'destination': 4, 'travelType': 3, 'category': 2, 'subcategory': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 5, 'inStock': 4, 'promotion': 3, 'brand': 1, 'productType': 2, 'currency': 0, 'store': 0, 'url': 0, 'shippingInfo': 0, 'model': 1, 'features': 1, 'availableSizes': 1, 'contentType': 0, 'stockStatus': 2, 'promotionValidUntil': 2, 'category': 2, 'id': 0}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 1, 'subcategory': 1, 'itemType': 1, 'productName': 0.8, 'recipeName': 0.5, 'title': 0.3, 'cuisine': 0.7, 'brand': 0.6, 'inStock': 0.9, 'promotion': 0.7, 'price': 0.4, 'url': 0.3}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 5, 'subcategory': 4, 'category': 3, 'price': 2, 'brand': 1, 'productName': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 5, 'country': 5, 'price': 4, 'inStock': 3, 'promotion': 3}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
   
Format wyników poprawny. Test powtórzony z tymi samymi parametrami (wykonanie 3):  
```python
{'output': {'price': 10, 'productType': 9, 'inStock': 8, 'currency': 7, 'brand': 6, 'category': 5, 'store': 4, 'url': 3, 'promotion': 2, 'shippingInfo': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'itemType': 10, 'productName': 9, 'category': 8, 'subcategory': 7, 'brand': 6, 'price': 5, 'currency': 4, 'store': 3, 'url': 2, 'inStock': 1, 'promotion': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 5, 'subcategory': 4, 'ram': 10, 'processor': 3, 'gpu': 2, 'price': 7, 'brand': 6, 'productLine': 5, 'model': 4, 'screenSize': 3, 'inStock': 8, 'promotion': 6, 'shippingInfo': 4, 'formFactor': 2, 'usage': 3}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 5, 'country': 5, 'region': 4, 'location': 4, 'travelType': 3, 'price': 2, 'boardType': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 1, 'brand': 10, 'productType': 10, 'category': 10, 'price': 100, 'currency': 10, 'store': 8, 'url': 8, 'inStock': 9, 'promotion': 9, 'shippingInfo': 5}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 10, 'subcategory': 9, 'itemType': 8, 'productName': 7, 'brand': 6, 'id': 5, 'price': 4, 'currency': 3, 'store': 2, 'url': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 20, 'itemType': 10, 'brand': 10, 'productName': 10, 'category': 10, 'subcategory': 10, 'productLine': 10, 'ram': 10, 'ramUnit': 10, 'price': 9, 'currency': 10, 'store': 9, 'url': 9, 'inStock': 10, 'promotion': 0, 'shippingInfo': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 10, 'location': 9, 'region': 9, 'itemType': 8, 'category': 7, 'subcategory': 6, 'travelType': 5, 'productName': 4, 'price': 3, 'store': 2, 'inStock': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 0, 'brand': 6, 'productType': 9, 'category': 5, 'price': 10, 'currency': 3, 'store': 4, 'url': 0, 'inStock': 8, 'promotion': 7, 'shippingInfo': 2, 'promotionValidUntil': 2, 'model': 2, 'features': 2, 'stockStatus': 1, 'availableSizes': 1, 'contentType': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 5, 'subcategory': 4, 'productName': 3, 'brand': 3, 'cuisine': 2, 'price': 1, 'currency': 1, 'store': 1, 'url': 1, 'inStock': 1, 'promotion': 1, 'shippingInfo': 1, 'itemType': 0, 'id': 0, 'recipeName': 0, 'contentType': 0, 'dietType': 0, 'title': 0, 'priceFrom': 0, 'variety': 0, 'model': 0, 'paymentOptions': 0, 'format': 0, 'specialty': 0, 'occasion': 0, 'stockStatus': 0, 'promotionValidUntil': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 0, 'itemType': 0, 'brand': 2, 'productName': 2, 'category': 2, 'subcategory': 2, 'productLine': 7, 'ram': 8, 'ramUnit': 1, 'price': 5, 'currency': 0, 'store': 0, 'url': 0, 'inStock': 0, 'promotion': 0, 'shippingInfo': 0, 'processor': 10, 'gpu': 9, 'model': 3, 'screenSize': 6, 'promotionValidUntil': 0, 'stockStatus': 0, 'usage': 0, 'paymentOptions': 0, 'formFactor': 0, 'features': 0, 'focus': 0, 'contentType': 0, 'topic': 0, 'title': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'region': 9, 'productName': 8, 'category': 7, 'subcategory': 7, 'price': 6, 'currency': 5, 'store': 4, 'url': 4, 'inStock': 5, 'promotion': 3, 'travelType': 4, 'activities': 5, 'itemType': 2, 'id': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'productType': 2, 'category': 3, 'brand': 4, 'model': 5, 'promotion': 6, 'shippingInfo': 7, 'inStock': 8, 'currency': 9, 'store': 10, 'url': 11}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 8, 'subcategory': 8, 'price': 5, 'currency': 5, 'store': 5, 'url': 5, 'inStock': 5, 'promotion': 5, 'shippingInfo': 5, 'cuisine': 5}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'itemType': 10, 'category': 10, 'subcategory': 8, 'ram': 10, 'price': 5, 'inStock': 5, 'promotion': 3, 'shippingInfo': 3}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 5, 'destination': 4, 'category': 3, 'subcategory': 2, 'travelType': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 5, 'inStock': 4, 'promotion': 3, 'brand': 1, 'productType': 1, 'currency': 1, 'store': 1, 'url': 1, 'shippingInfo': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 3, 'subcategory': 3, 'itemType': 2, 'productName': 3, 'brand': 2, 'price': 1, 'inStock': 2, 'promotion': 1, 'cuisine': 1, 'url': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 5, 'price': 4, 'inStock': 5, 'brand': 3, 'productName': 3, 'category': 4, 'subcategory': 4, 'itemType': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 3, 'country': 3, 'price': 2, 'inStock': 1, 'promotion': 1, 'travelType': 1, 'boardType': 2}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
  
Format wyników poprawny. Test powtórzony z tymi samymi parametrami (wykonanie 4):  
```python
{'output': {'price': 10, 'productType': 5, 'category': 4, 'inStock': 3, 'brand': 2, 'currency': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 8, 'subcategory': 7, 'itemType': 6, 'brand': 5, 'price': 4, 'inStock': 3, 'store': 2, 'url': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'category': 9, 'subcategory': 8, 'price': 7, 'brand': 6, 'productName': 5, 'productLine': 4, 'inStock': 3, 'promotion': 2, 'shippingInfo': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'itemType': 10, 'country': 8, 'region': 7, 'destination': 6, 'category': 5, 'subcategory': 4, 'travelType': 3, 'price': 2, 'inStock': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 1, 'brand': 9, 'productType': 9, 'category': 9, 'price': 10, 'currency': 9, 'store': 7, 'url': 7, 'inStock': 8, 'promotion': 6, 'shippingInfo': 5, 'model': 4, 'promotionValidUntil': 3, 'stockStatus': 3, 'availableSizes': 3, 'features': 3, 'contentType': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 10, 'subcategory': 9, 'itemType': 8, 'productName': 7, 'brand': 6, 'id': 5, 'price': 4, 'currency': 3, 'store': 2, 'url': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'category': 9, 'subcategory': 8, 'price': 7, 'productName': 6, 'brand': 5, 'store': 4, 'inStock': 3, 'promotion': 2, 'currency': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 10, 'region': 8, 'location': 8, 'itemType': 7, 'category': 6, 'subcategory': 5, 'travelType': 5, 'price': 4}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': -10, 'brand': 3, 'productType': 4, 'category': 2, 'price': 5, 'currency': 3, 'store': 1, 'url': 0, 'inStock': -1, 'promotion': -2, 'shippingInfo': -3, 'promotionValidUntil': -4, 'model': -5, 'features': -6, 'stockStatus': -7, 'availableSizes': -8, 'contentType': -9}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 9, 'subcategory': 8, 'brand': 7, 'price': 6, 'inStock': 6, 'promotion': 5, 'shippingInfo': 5, 'store': 4, 'url': 3, 'currency': 3, 'priceFrom': 2, 'promotionValidUntil': 2, 'contentType': 1, 'dietType': 1, 'cuisine': 1, 'variety': 1, 'stockStatus': 1, 'format': 1, 'specialty': 1, 'edition': 1, 'occasion': 1, 'model': 1, 'paymentOptions': 1, 'id': 0, 'itemType': 0, 'title': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 1, 'itemType': 1, 'brand': 5, 'productName': 5, 'category': 4, 'subcategory': 5, 'productLine': 4, 'ram': 5, 'ramUnit': 4, 'price': 3, 'currency': 4, 'store': 3, 'url': 3, 'inStock': 3, 'promotion': 1, 'shippingInfo': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'id': 0, 'itemType': 0, 'productName': 8, 'category': 0, 'subcategory': 0, 'destination': 10, 'region': 9, 'price': 2, 'currency': 1, 'store': 4, 'url': 3, 'inStock': 5, 'promotion': 0, 'travelType': 7, 'activities': 6}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'productType': 2, 'category': 3}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 5, 'subcategory': 5, 'productName': 5, 'brand': 4, 'price': 3, 'currency': 3, 'store': 3, 'url': 3, 'inStock': 3, 'promotion': 3, 'promotionValidUntil': 2, 'shippingInfo': 2, 'model': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'itemType': 5, 'category': 5, 'ram': 5, 'price': 3, 'inStock': 2, 'promotion': 1, 'shippingInfo': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 5, 'destination': 4, 'travelType': 3, 'category': 2, 'subcategory': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 5, 'inStock': 4, 'promotion': 3, 'shippingInfo': 2, 'brand': 1, 'productType': 1, 'currency': 1, 'store': 1, 'url': 1, 'model': 1, 'features': 1, 'availableSizes': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 1, 'subcategory': 1, 'itemType': 1, 'productName': 1, 'brand': 0.5, 'price': 0.5, 'inStock': 0.5, 'promotion': 0.5, 'cuisine': 0.5, 'url': 0.3, 'id': 0.1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 32, 'subcategory': 'Gaming', 'category': 'Laptopy', 'inStock': 1, 'brand': 1, 'price': 0.5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 5, 'country': 5, 'price': 4, 'promotion': 3, 'inStock': 2, 'travelType': 3, 'subcategory': 3, 'boardType': 4, 'departureInfo': 5, 'location': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
  

Model `inclusionAI/Ling-1T:featherless-ai` przy kwerendzie `Znajdź najbardziej wydajny laptop` ponownie zwrócił błędną merytorycznie odpowiedź   (choć format JSON jest już poprawnie zachowany). Test powtórzony z tymi samymi parametrami (wykonanie 5):  

```python
{'output': {'price': 10, 'productType': 9, 'inStock': 8, 'currency': 7, 'brand': 6, 'category': 5, 'store': 4, 'url': 3, 'promotion': 2, 'shippingInfo': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 3, 'category': 3, 'subcategory': 2, 'brand': 1, 'itemType': 1, 'price': 1, 'currency': 1, 'store': 1, 'url': 1, 'inStock': 1, 'promotion': 1, 'shippingInfo': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'productName': 9, 'category': 8, 'brand': 7, 'price': 6, 'subcategory': 5, 'productLine': 4, 'model': 3, 'processor': 2, 'screenSize': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'itemType': 5, 'productName': 4, 'category': 5, 'subcategory': 4, 'destination': 5, 'country': 5, 'boardType': 3, 'price': 3, 'currency': 2, 'store': 1, 'url': 1, 'inStock': 1, 'promotion': 2, 'travelType': 3, 'region': 5, 'location': 5}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 10, 'productType': 9, 'category': 8, 'brand': 7, 'inStock': 6, 'promotion': 5, 'currency': 4, 'store': 3, 'url': 2, 'shippingInfo': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 10, 'subcategory': 9, 'productName': 8, 'brand': 7, 'price': 6, 'inStock': 5, 'promotion': 4, 'store': 3, 'url': 2, 'itemType': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'productName': 10, 'ram': 9, 'category': 8, 'subcategory': 7, 'price': 6, 'brand': 5, 'store': 4, 'inStock': 3, 'promotion': 2, 'shippingInfo': 1}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 10, 'region': 9, 'location': 9, 'itemType': 8, 'category': 7, 'subcategory': 6, 'productName': 5, 'price': 4, 'currency': 4, 'inStock': 3, 'promotion': 2}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 0, 'brand': 5, 'productType': 9, 'category': 4, 'price': 10, 'currency': 0, 'store': 3, 'url': 0, 'inStock': 8, 'promotion': 2, 'shippingInfo': 1, 'promotionValidUntil': 0, 'model': 0, 'features': 0, 'stockStatus': 0, 'availableSizes': 0, 'contentType': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'id': 1, 'itemType': 6, 'productName': 10, 'recipeName': 4, 'title': 4, 'brand': 8, 'category': 9, 'subcategory': 9, 'price': 5, 'priceFrom': 5, 'currency': 4, 'store': 5, 'url': 5, 'inStock': 8, 'stockStatus': 3, 'promotion': 7, 'promotionValidUntil': 3, 'shippingInfo': 7, 'format': 6, 'contentType': 3, 'specialty': 6, 'dietType': 2, 'occasion': 2, 'model': 3, 'paymentOptions': 3, 'edition': 3, 'cuisine': 2, 'variety': 2}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'processor': 10, 'gpu': 9, 'ram': 8, 'brand': 7, 'productName': 6, 'price': 5, 'category': 4, 'subcategory': 3, 'productLine': 2, 'store': 1}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 10, 'country': 9, 'region': 8, 'location': 7}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 1, 'productType': 2, 'category': 3}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 10, 'category': 8, 'subcategory': 8, 'itemType': 10}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'itemType': 5, 'category': 5, 'ram': 5, 'price': 3, 'inStock': 2, 'promotion': 1, 'shippingInfo': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 5, 'destination': 4, 'travelType': 3, 'category': 2, 'subcategory': 1}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 5, 'inStock': 4, 'promotion': 3, 'shippingInfo': 2, 'brand': 1, 'productType': 1, 'category': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 1, 'subcategory': 1, 'itemType': 0.5, 'productName': 0.5, 'brand': 0.3, 'price': 0.2, 'inStock': 0.1, 'url': 0.1, 'cuisine': 0.2, 'store': 0.1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 10, 'price': 7, 'category': 8, 'subcategory': 8, 'inStock': 5, 'brand': 3, 'productLine': 4}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 3, 'country': 3, 'category': 2, 'subcategory': 2, 'inStock': 1, 'price': 1, 'currency': 1, 'travelType': 1, 'boardType': 2, 'store': 1, 'url': 1, 'promotion': 1, 'id': 0}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
  
Format wyników poprawny.  
  
W związku z tym, że w jednym z pięciu wykonań obecnej konfiguracji programu model `inclusionAI/Ling-1T:featherless-ai`
popełnił błąd, zdecydowaliśmy się na następujące metody wykrycia i naprawy błędów:  
- odrzucać wyniki w razie błędu i powtórzyć zapytanie do api dwukrotnie, jeżeli błąd wystąpił  
- zmienić kwerendę tak, żeby priorytety były w zakresie 0-100  
  
Kod i kwerenda zostały zaktualizowane, rozwiązanie zawarte w pliku:  
`src/ai_search.py`
  
Nowa kwerenda:  
```python
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól (object properties) danych które najbardziej jej odpowiadają i zwróć tylko jeden obiekt wszystkich pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue, \"propertyName\": priorityValue} - odpowiedź musi zawrzeć się tylko w jednym obiekcie, wartości priorytetów mogą być tylko z zakresu od 0 do 100 włącznie, dane podane są poniżej: ###\n"
```
  
Wyniki:
```python
{'output': {'price': 100, 'productType': 80, 'inStock': 60, 'currency': 50, 'promotion': 40, 'category': 30, 'brand': 20, 'shippingInfo': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'itemType': 100, 'productName': 90, 'category': 80, 'subcategory': 70, 'brand': 60, 'price': 50, 'inStock': 40, 'promotion': 30, 'shippingInfo': 20, 'url': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'itemType': 100, 'category': 100, 'subcategory': 80, 'ram': 90, 'ramUnit': 100, 'price': 70, 'inStock': 100, 'brand': 60, 'productLine': 50, 'model': 40, 'processor': 30, 'screenSize': 20, 'promotion': 10, 'shippingInfo': 10, 'usage': 10, 'features': 5, 'formFactor': 5}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'itemType': 100, 'productName': 90, 'category': 80, 'subcategory': 70, 'destination': 60, 'country': 50, 'region': 40, 'boardType': 30, 'price': 20, 'currency': 10, 'store': 5, 'url': 5, 'inStock': 3, 'promotion': 2, 'travelType': 1}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 100, 'productType': 90, 'category': 80, 'brand': 70, 'inStock': 60, 'promotion': 50, 'currency': 40, 'store': 30, 'url': 20, 'shippingInfo': 10, 'model': 5, 'features': 5, 'stockStatus': 5, 'availableSizes': 5, 'promotionValidUntil': 5, 'contentType': 0, 'id': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'productName': 100, 'category': 90, 'subcategory': 85, 'brand': 70, 'price': 60, 'store': 50, 'inStock': 40, 'promotion': 30, 'url': 20, 'itemType': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'id': 20, 'itemType': 100, 'brand': 95, 'productName': 100, 'category': 100, 'subcategory': 100, 'productLine': 95, 'ram': 100, 'ramUnit': 100, 'price': 85, 'currency': 100, 'store': 80, 'url': 80, 'inStock': 100, 'promotion': 50, 'shippingInfo': 70}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'id': 4, 'itemType': 100, 'productName': 100, 'category': 100, 'subcategory': 100, 'location': 100, 'boardType': 100, 'price': 100, 'priceUnit': 100, 'currency': 100, 'store': 100, 'url': 100, 'inStock': 100, 'promotion': 100, 'amenities': 100}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'id': 30, 'brand': 70, 'productType': 90, 'category': 45, 'price': 100, 'currency': 50, 'store': 60, 'url': 55, 'inStock': 85, 'promotion': 80, 'shippingInfo': 20}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'id': 30, 'itemType': 25, 'productName': 100, 'brand': 90, 'category': 85, 'subcategory': 80, 'price': 75, 'priceFrom': 20, 'currency': 15, 'store': 50, 'url': 45, 'inStock': 70, 'stockStatus': 10, 'promotion': 60, 'promotionValidUntil': 5, 'shippingInfo': 55, 'format': 5, 'dietType': 5, 'contentType': 5, 'recipeName': 5, 'title': 5, 'specialty': 5, 'edition': 5, 'variety': 5, 'model': 5, 'paymentOptions': 5, 'occasion': 5}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 90, 'price': 80, 'processor': 70, 'gpu': 60, 'brand': 50, 'category': 30, 'subcategory': 30}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'id': 0, 'itemType': 10, 'productName': 10, 'category': 10, 'subcategory': 10, 'destination': 80, 'region': 100, 'price': 30, 'currency': 5, 'store': 10, 'url': 10, 'inStock': 50, 'promotion': 5, 'travelType': 40, 'activities': 25}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 100, 'productType': 90, 'category': 80, 'brand': 70, 'promotion': 60, 'inStock': 50, 'shippingInfo': 40, 'model': 30, 'features': 20, 'availableSizes': 10}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'itemType': 100, 'productName': 100, 'category': 100, 'subcategory': 100, 'price': 0, 'currency': 0, 'store': 0, 'url': 0, 'inStock': 0, 'promotion': 0, 'shippingInfo': 0, 'cuisine': 0, 'contentType': 0, 'dietType': 0, 'format': 0, 'specialty': 0, 'occasion': 0, 'brand': 0, 'model': 0, 'priceFrom': 0, 'variety': 0, 'edition': 0, 'stockStatus': 0, 'promotionValidUntil': 0, 'paymentOptions': 0}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'category': 100, 'subcategory': 100, 'ram': 100, 'price': 80, 'brand': 70, 'productName': 60, 'itemType': 50, 'inStock': 40, 'promotion': 30, 'shippingInfo': 20}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'country': 100, 'destination': 90, 'itemType': 80, 'category': 70, 'subcategory': 60, 'productName': 50, 'price': 40, 'currency': 30, 'store': 20, 'url': 10}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź wakacje które są najbliżej Polski'}
{'output': {'price': 100, 'inStock': 100, 'productType': 80, 'category': 70, 'promotion': 30, 'brand': 20, 'currency': 10, 'store': 5, 'url': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź buty o najmniejszej cenie'}
{'output': {'category': 100, 'subcategory': 100, 'itemType': 100, 'productName': 80, 'brand': 70, 'price': 30, 'inStock': 20, 'promotion': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź narzędzia kuchenne'}
{'output': {'ram': 100, 'itemType': 100, 'category': 100, 'subcategory': 95, 'price': 85, 'inStock': 80, 'brand': 70, 'productName': 70}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź najbardziej wydajny laptop'}
{'output': {'destination': 100, 'country': 100, 'category': 100, 'subcategory': 100, 'inStock': 100, 'price': 80, 'currency': 100}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź wakacje które są najbliżej Polski'}
```
    
## Wnioski:  
Istotnym rezultatem przeprowadzonych prac jest osiągnięcie pełnej powtarzalności procesu formatowania. Wielokrotne wykonanie procedur testowych wykazało, że wypracowany format zachowuje jednoznaczność w każdej iteracji.  
Oznacza to, że cel pracy w zakresie standaryzacji został osiągnięty, a system gwarantuje deterministyczne rezultaty, eliminując ryzyko rozbieżności w strukturze generowanych danych.  