# Raport 2

Test priorytetów pól obiektów w bazie danych

15.11.2025
## 1. Wprowadzenie
W ramach drugiego raportu przetestowaliśmy modele AI pod kątem ustalania priorytetów pól
w nowym, bardziej rozbudowanym formacie bazy danych. Dotychczasowe obiekty w bazie
miały postać:
```json
{
"id": x,
"data": y
}
```
Nowy format obiektów zawierał wiele dodatkowych pól, np.:
```json
{
"id": 24,
"itemType": "product",
"brand": "ASUS",
"productName": "Laptop ASUS TUF",
"category": "Laptopy",
"subcategory": "Gaming",
"productLine": "TUF",
"ram": 16,
"ramUnit": "GB",
"price": 4999,
"currency": "PLN",
"store": "asuspolska.pl",
"url": "www.asuspolska.pl",
"inStock": true,
"stockStatus": "Wysyłka 24H",
"promotion": false,
"shippingInfo": "Wysyłka 24H"
}
```
Celem testów było sprawdzenie, czy modele prawidłowo rozpoznają najważniejsze pola
odpowiadające kwerendzie (np. najtańsze buty, narzędzia kuchenne, najwydajniejsze laptopy,
wakacje).
## 2. Test modelu inclusionAI/Ling-1T:featherless-ai
Najpierw wykonaliśmy test dla modelu inclusionAI/Ling-1T:featherless-ai, by sprawdzić czy
zapewni miarodajny rezultat.
Wynik:
```json
[
{
"query": "Znajdź najtańsze buty",
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"price": 5,
"promotion": 4,
"inStock": 3,
"productType": 2,
"brand": 1,
"currency": 0,
"store": 0,
"url": 0,
"shippingInfo": 0
}
},
{
"query": "Znajdź tylko narzędzia kuchenne",
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"category": 3,
"subcategory": 3,
"itemType": 2,
"productName": 3,
"brand": 2,
"price": 1,
"inStock": 1,
"promotion": 1,
"url": 1,
"store": 1,
"cuisine": 1
}
},
{
"query": "Znajdź najwydajniejszy laptop",
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"category": 3,
"subcategory": 3,
"ram": 3,
"price": 2,
"brand": 2,
"productName": 2,
"itemType": 1,
"inStock": 1,
"promotion": 1
}
},
{
"query": "Znajdź wakacje najbliżej Polski",
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"destination": 5,
"country": 5,
"price": 4,
"currency": 4,
"inStock": 3,
"promotion": 3,
"travelType": 3,
"boardType": 3,
"location": 2,
"region": 2,
"url": 1,
"store": 1
}
}
]
```
Zapytanie Najwyższe priorytety według modelu

Znajdź najtańsze buty price

Znajdź tylko narzędzia kuchenne category, subcategory, productName

Znajdź najwydajniejszy laptop category, subcategory, ram

Znajdź wakacje najbliżej Polski destination, country

Wniosek:
Części obiektu o najwyższych priorytetach w większości odpowiadały kwerendzie z main.py.
Model skutecznie identyfikował pola kluczowe dla zapytania, choć pomijał niektóre
dodatkowe informacje (np. pola bez ceny). Priorytety były ogólnie celne, choć brakowało
pełnej spójności w formacie wyjścia.

## 3. Testy pozostałych modeli
Przeprowadziliśmy testy dla wszystkich wcześniej użytych modeli, by sprawdzić czy
ustalanie priorytetów z pomocą AI zadziała poprawnie.
Otrzymaliśmy takie wyniki:
```json
[
{
"query": "Znajdź najtańsze buty",
"models": [
{
"model": "deepseek-ai/DeepSeek-V3-0324",
"output": {
"price": 10,
"productType": 9,
"inStock": 8,
"currency": 7,
"brand": 6,
"category": 5,
"promotion": 4,
"shippingInfo": 3,
"store": 2,
"url": 1
}
},
{
"model": "moonshotai/Kimi-K2-Instruct-0905",
"output": {
"price": 10,
"currency": 9,
"productType": 8,
"inStock": 7,
"promotion": 6,
"brand": 5,
"category": 4,
"store": 3,
"url": 2,
"shippingInfo": 1
}
},
{
"model": "meta-llama/Llama-3.1-8B-Instruct",
"output": [
{"field": "price", "priority": 1},
{"field": "brand", "priority": 2},
{"field": "category", "priority": 3},
{"field": "productType", "priority": 4},
{"field": "inStock", "priority": 5},
{"field": "shippingInfo", "priority": 6}
]
},
{
"model": "openai/gpt-oss-20b:groq",
"output": {
"price": 1,
"productType": 2,
"inStock": 3,
"category": 4,
"brand": 5,
"promotion": 6,
"store": 7,
"shippingInfo": 8
}
},
{
"model": "CohereLabs/command-a-translate-08-2025:cohere",
"output": [
{"field": "price", "priority": 1},
{"field": "productType", "priority": 2},
{"field": "category", "priority": 3},
{"field": "promotion", "priority": 4},
{"field": "shippingInfo", "priority": 5}
]
},
{
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"price": 5,
"inStock": 4,
"promotion": 3,
"productType": 3,
"category": 2,
"brand": 2,
"shippingInfo": 1,
"currency": 0,
"store": 0,
"url": 0,
"model": 0,
"features": 0,
"availableSizes": 0,
"stockStatus": 0,
"promotionValidUntil": 0,
"contentType": 0,
"id": 0
}
}
]
},
{
"query": "Znajdź tylko narzędzia kuchenne",
"models": [
{
"model": "deepseek-ai/DeepSeek-V3-0324",
"output": [
{"field": "category", "priority": 5},
{"field": "subcategory", "priority": 4},
{"field": "productName", "priority": 3},
{"field": "brand", "priority": 2},
{"field": "itemType", "priority": 1}
]
},
{
"model": "moonshotai/Kimi-K2-Instruct-0905",
"output": [
{"productName": 10},
{"category": 9},
{"subcategory": 9},
{"brand": 8},
{"itemType": 8},
{"id": 1}
]
},
{
"model": "meta-llama/Llama-3.1-8B-Instruct",
"output": [
{"field": "category", "priority": 2},
{"field": "subcategory", "priority": 1}
]
},
{
"model": "openai/gpt-oss-20b:groq",
"output": {
"productName": 10,
"brand": 9,
"category": 8,
"subcategory": 7,
"price": 6,
"store": 5,
"inStock": 4,
"promotion": 3,
"shippingInfo": 2,
"currency": 1
}
},
{
"model": "CohereLabs/command-a-translate-08-2025:cohere",
"output": {
"category": 1,
"subcategory": 1,
"productName": 1,
"brand": 0.8,
"price": 0.7,
"currency": 0.7,
"store": 0.6,
"url": 0.5,
"inStock": 0.4,
"promotion": 0.3,
"shippingInfo": 0.2
}
},
{
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"subcategory": 3,
"category": 2,
"productName": 3,
"itemType": 3,
"brand": 2,
"id": 1
}
}
]
}
]
```
Wnioski:
Trafność najwyższych priorytetów:
Części obiektu, które modele uznawały za najwyższe priorytety, w większości odpowiadały
kwerendzie z main.py. Na przykład w zapytaniu „Znajdź najtańsze buty” pola price,
promotion i inStock były konsekwentnie traktowane jako kluczowe, co jest zgodne z logiką
zapytania. W przypadku bardziej złożonych zapytań (np. „Znajdź wakacje najbliżej Polski”)
modele wskazywały różne kombinacje pól (destination, country, price, currency, inStock),
które w większości również miały sens w kontekście kwerendy.
Celność decyzji o priorytecie:
Decyzje modeli były częściowo celne – w większości przypadków kluczowe pola dla
zapytania były prawidłowo wskazane. Jednak niektóre dodatkowe atrybuty (np.
promotionValidUntil, stockStatus) były pomijane lub uzyskiwały bardzo niskie priorytety, co
może prowadzić do niepełnej interpretacji danych.
Rozbieżności między modelami:
Wyniki między modelami nie pokrywały się w pełni. Różnice obejmowały zarówno kolejność
priorytetów, jak i format wyjścia – modele zwracały dane w formacie JSON, Python dict, a
czasem list obiektów. Skale priorytetów również były różne: 1–10, 0–1. Często różnice w
priorytetach pomiędzy modelami wynosiły 1–2 punkty, co wskazuje na brak pełnej spójności
w rankingowaniu pól.
Sprawdziliśmy czy po użyciu synonimicznej kwerendy odpowiedź modelu się nie zmieni:
```json
[
{
"query": "Znajdź buty o najmniejszej cenie",
"models": [
{
"model": "deepseek-ai/DeepSeek-V3-0324",
"output": {
"price": 10,
"productType": 9,
"inStock": 8,
"currency": 7,
"brand": 6,
"category": 5,
"store": 4,
"url": 3,
"promotion": 2,
"shippingInfo": 1,
"model": 0,
"features": 0,
"availableSizes": 0,
"promotionValidUntil": 0,
"stockStatus": 0,
"contentType": 0
}
},
{
"model": "moonshotai/Kimi-K2-Instruct-0905",
"output": {
"price": 10,
"productType": 9,
"category": 8,
"inStock": 7,
"promotion": 6,
"brand": 5,
"store": 4,
"currency": 3,
"shippingInfo": 2,
"features": 1
}
},
{
"model": "meta-llama/Llama-3.1-8B-Instruct",
"output": [
{"field": "price", "priority": 1},
{"field": "id", "priority": 2}
]
},
{
"model": "openai/gpt-oss-20b:groq",
"output": {
"price": 5,
"productType": 4,
"brand": 3,
"category": 2,
"store": 1
}
},
{
"model": "CohereLabs/command-a-translate-08-2025:cohere",
"output": [
{"field": "price", "priority": 1},
{"field": "productType", "priority": 2},
{"field": "category", "priority": 3},
{"field": "promotion", "priority": 4},
{"field": "inStock", "priority": 5}
]
},
{
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"price": 5,
"inStock": 4,
"promotion": 3,
"brand": 2,
"productType": 2,
"store": 1,
"currency": 1,
"url": 1,
"shippingInfo": 1,
"model": 1
}
}
]
},
{
"query": "Znajdź narzędzia kuchenne",
"models": [
{
"model": "deepseek-ai/DeepSeek-V3-0324",
"output": {
"itemType": 1,
"productName": 1,
"category": 1,
"subcategory": 1,
"brand": 0.8,
"price": 0.5,
"currency": 0.5,
"store": 0.3,
"url": 0.3,
"inStock": 0.2,
"promotion": 0.1,
"shippingInfo": 0.1
}
},
{
"model": "moonshotai/Kimi-K2-Instruct-0905",
"output": [
{"field": "category", "priority": 10},
{"field": "subcategory", "priority": 9},
{"field": "productName", "priority": 8},
{"field": "brand", "priority": 7},
{"field": "itemType", "priority": 6},
{"field": "price", "priority": 5},
{"field": "store", "priority": 4},
{"field": "inStock", "priority": 3},
{"field": "promotion", "priority": 2},
{"field": "shippingInfo", "priority": 1}
]
},
{
"model": "meta-llama/Llama-3.1-8B-Instruct",
"output": [
{
"subcategory": 0.25,
"category": 0.25,
"price": -0.25,
"productName": -0.25,
"brand": -0.25,
"cuisine": -0.25,
"url": -0.25,
"contentType": -0.25
}
]
},
{
"model": "openai/gpt-oss-20b:groq",
"output": {
"productName": 10,
"brand": 9,
"category": 8,
"subcategory": 7,
"price": 6,
"currency": 5,
"store": 4,
"url": 3,
"inStock": 2,
"promotion": 1,
"shippingInfo": 0,
"promotionValidUntil": -1,
"format": -2,
"model": -3,
"contentType": -4,
"cuisine": -5,
"dietType": -6,
"specialty": -7,
"occasion": -8,
"edition": -9,
"stockStatus": -10,
"priceFrom": -11,
"paymentOptions": -12,
"id": -13,
"itemType": -14
}
},
{
"model": "CohereLabs/command-a-translate-08-2025:cohere",
"output": {
"category": 1,
"subcategory": 1,
"productName": 1,
"brand": 0.8,
"price": 0.7,
"currency": 0.6,
"store": 0.5,
"url": 0.4,
"inStock": 0.3,
"promotion": 0.2,
"shippingInfo": 0.1
}
},
{
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"category": 3,
"subcategory": 3,
"itemType": 2,
"productName": 2,
"price": 1,
"currency": 1,
"inStock": 1,
"promotion": 1,
"brand": 1,
"url": 1,
"store": 1
}
}
]
},
{
"query": "Znajdź najbardziej wydajny laptop",
"models": [
{
"model": "deepseek-ai/DeepSeek-V3-0324",
"output": {
"category": 10,
"subcategory": 8,
"ram": 10,
"ramUnit": 8,
"price": 6,
"currency": 5,
"brand": 7,
"productName": 9,
"productLine": 6,
"model": 5,
"processor": 4,
"screenSize": 3,
"inStock": 4,
"promotion": 3,
"shippingInfo": 2,
"usage": 2,
"formFactor": 1,
"features": 1
}
},
{
"model": "moonshotai/Kimi-K2-Instruct-0905",
"output": {
"productName": 10,
"ram": 9,
"category": 8,
"processor": 7,
"subcategory": 6,
"model": 5,
"productLine": 4,
"brand": 3,
"price": 2,
"id": 1
}
},
{
"model": "meta-llama/Llama-3.1-8B-Instruct",
"output": {
"fields": [
{"name": "ram", "priority": 3},
{"name": "price", "priority": 2},
{"name": "brand", "priority": 1},
{"name": "category", "priority": 1},
{"name": "subcategory", "priority": 1},
{"name": "productLine", "priority": 1},
{"name": "screenSize", "priority": 1},
{"name": "processor", "priority": 1},
{"name": "model", "priority": 1},
{"name": "gpu", "priority": 1},
{"name": "inStock", "priority": 1},
{"name": "promotion", "priority": 1},
{"name": "formFactor", "priority": 1},
{"name": "features", "priority": 1},
{"name": "usage", "priority": 1},
{"name": "stockStatus", "priority": 1}
]
}
},
{
"model": "openai/gpt-oss-20b:groq",
"output": {
"processor": 1,
"gpu": 2,
"ram": 3,
"price": 4,
"brand": 5
}
},
{
"model": "CohereLabs/command-a-translate-08-2025:cohere",
"output": {
"category": 3,
"subcategory": 3,
"ram": 2,
"price": 1,
"brand": 1,
"productName": 1,
"inStock": 1
}
},
{
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"brand": 3,
"productName": 3,
"category": 3,
"subcategory": 3,
"ram": 3,
"price": 2,
"inStock": 2,
"promotion": 1,
"store": 1,
"url": 1,
"shippingInfo": 1
}
}
]
},
{
"query": "Znajdź wakacje które są najbliżej Polski",
"models": [
{
"model": "deepseek-ai/DeepSeek-V3-0324",
"output": {
"country": 10,
"destination": 9,
"region": 8,
"location": 7,
"itemType": 6,
"category": 5,
"subcategory": 4,
"travelType": 3,
"price": 2,
"currency": 1
}
},
{
"model": "moonshotai/Kimi-K2-Instruct-0905",
"output": {
"destination": 10,
"country": 9,
"location": 8,
"region": 7,
"itemType": 6,
"category": 5,
"subcategory": 4,
"travelType": 3,
"productName": 2,
"price": 1
}
},
{
"model": "meta-llama/Llama-3.1-8B-Instruct",
"output": [
{"field": "destination","priority":1},
{"field": "country","priority":2},
{"field": "category","priority":3}
]
},
{
"model": "openai/gpt-oss-20b:groq",
"output": {
"destination": 100,
"country": 95,
"region": 90,
"travelType": 80,
"subcategory": 70,
"boardType": 60,
"price": 50,
"promotion": 40,
"inStock": 30
}
},
{
"model": "CohereLabs/command-a-translate-08-2025:cohere",
"output": {
"country": 5,
"destination": 4,
"region": 3,
"location": 2,
"category": 1
}
},
{
"model": "inclusionAI/Ling-1T:featherless-ai",
"output": {
"destination": 3,
"country": 3,
"price": 2,
"inStock": 2,
"promotion": 1,
"travelType": 1,
"boardType": 1,
"url": 1
}
}
]
}
]
```
### Stabilność przy synonimicznych zapytaniach:
Użycie synonimów (np. „Znajdź buty o najmniejszej cenie”) pokazało, że niektóre modele
zmieniały szczegółowo priorytety i format wyjścia – output czasami przyjmował różne skale,
np. 1–10 lub 0–0,5–1. Poza tym różne modele nadawały nieco odmienne priorytety tym
samym polom. Mimo to ogólna logika wyboru najważniejszych pól pozostawała podobna –
kluczowe atrybuty nadal były wskazywane jako istotne, choć z drobnymi różnicami w
kolejności i skali, a niektóre priorytety były przesunięte o 1–2 punkty. Oznacza to, że nie
można liczyć na całkowicie jednoznaczny wynik, jednak generalny układ priorytetów
pozostaje spójny.
### Wniosek:
Ogólnie można uznać, że modele potrafią wskazać główne pola odpowiadające zapytaniom,
ale wyniki są niejednorodne i nie w pełni stabilne. Decyzja o priorytetach jest w większości
przypadków sensowna, jednak różnice w formatowaniu i skali priorytetów utrudniają
porównywanie wyników między modelami i wymuszają ujednolicenie danych przed dalszą
analizą.

## 4. Analiza porównawcza modeli
Finalnie sprawdziliśmy czy ta sama kwerenda zapewni ten sam wynik:
```json
{
"buty_o_najnizszej_cenie": {
"price": 1,
"productType": 0.9,
"inStock": 0.8,
"brand": 0.7,
"category": 0.6,
"store": 0.5,
"currency": 0.4,
"promotion": 0.3,
"url": 0.2,
"shippingInfo": 0.1
},
"narzedzia_kuchenne": {
"category": 1,
"subcategory": 0.9,
"productName": 0.8,
"brand": 0.7,
"itemType": 0.6,
"price": 0.5,
"inStock": 0.4,
"url": 0.3,
"store": 0.2,
"promotion": 0.1
},
"najbardziej_wydajny_laptop": {
"category": 1,
"ram": 0.9,
"productName": 0.85,
"processor": 0.8,
"ramUnit": 0.75,
"model": 0.7,
"productLine": 0.65,
"brand": 0.6,
"price": 0.55,
"inStock": 0.5,
"promotion": 0.4,
"shippingInfo": 0.35,
"features": 0.3,
"formFactor": 0.25,
"usage": 0.2,
"stockStatus": 0.15
},
"wakacje_najblizej_polski": {
"destination": 1,
"country": 0.95,
"location": 0.9,
"region": 0.85,
"itemType": 0.8,
"category": 0.75,
"subcategory": 0.7,
"travelType": 0.65,
"price": 0.6,
"currency": 0.55,
"promotion": 0.5,
"inStock": 0.45,
"store": 0.4,
"url": 0.35
}
}
```
## Modele bardziej spójne i wiarygodne:

### 1. deepseek-ai/DeepSeek-V3-0324
- Priorytety pól były stabilne i spójne z logiką zapytań (price, inStock, category itd.).
- Format odpowiedzi w większości przypadków JSON – łatwy do interpretacji.
- Pokrycie pól było kompletne, w tym dla bardziej złożonych zapytań jak „Znajdź wakacje najbliżej Polski”.

### 2. moonshotai/Kimi-K2-Instruct-0905
- Trafnie wskazywał główne pola dla większości zapytań.
- Skala priorytetów różniła się od DeepSeek, ale ogólna kolejność głównych atrybutów była sensowna.
- Format JSON, spójny, chociaż mniej szczegółowy przy niektórych polach dodatkowych.

## Modele umiarkowanie spójne:

### 1. openai/gpt-oss-20b:groq
- Wskazuje najważniejsze pola, ale priorytety są czasami odwrócone (np. dla laptopów processor > price).
- Format wyjścia w JSON, ale brak pełnego pokrycia niektórych pól dodatkowych (promotion, shippingInfo).
- Można polegać na głównych atrybutach, ale nie na szczegółowych rankingach.

## Modele mniej spójne i mniej wiarygodne:

### 1. meta-llama/Llama-3.1-8B-Instruct
- Nie zawsze wskazuje wszystkie pola kluczowe (często tylko kilka najważniejszych).
- Priorytety nie są stabilne – różne zapytania mają bardzo różną skalę i liczbę pól.
- Format mieszany (JSON, listy obiektów), trudny do automatycznego przetwarzania.

### 2. CohereLabs/command-a-translate-08-2025
- Często zmienia format wyjścia (lista, JSON).
- Nie zawsze uwzględnia wszystkie kluczowe pola.
- Priorytety dla bardziej złożonych zapytań nie zawsze sensowne.

### 3. inclusionAI/Ling-1T:featherless-ai
- Poprawnie wskazuje kluczowe pola, ale wprowadza liczne rozbieżności w priorytetach i wartościach (niekiedy wszystkie pola mają podobny priorytet).
- Format i liczby priorytetów różnią się znacznie między zapytaniami.
- Wyniki trudne do bezpośredniego porównania i automatycznej analizy.

### 5. Wnioski końcowe
#### Stabilność wyników
- Brak jednoznacznego wyniku – kolejność i skala priorytetów różniły się między modelami, a czasem także przy synonimicznych zapytaniach.
- Większość modeli prawidłowo rozpoznaje kluczowe pola, np. price dla „najtańsze buty” czy ram/processor dla „najwydajniejszy laptop”, ale dokładne priorytety nie zawsze się zgadzają.
#### Format odpowiedzi
- Pojawiły się trudności z formatowaniem: JSON, Python dict, lista obiektów – utrudnia to automatyczne przetwarzanie wyników.
- Niektóre modele zmieniają strukturę odpowiedzi w zależności od zapytania lub użytych synonimów.
#### Zalecenia
- Testy lepiej przeprowadzać na bardziej ustrukturyzowanej bazie danych, aby jednoznacznie ocenić trafność priorytetów i spójność wyników.
- Przy niejednorodnym formacie odpowiedzi warto stosować normalizację wyników przed analizą porównawczą.
#### Zalety podejścia
- Modele AI szybko wskazują pola najbardziej istotne dla zapytania.
- Większość modeli logicznie rozpoznaje główne atrybuty.
- Możliwe jest stosowanie synonimicznych zapytań bez dużego spadku trafności dla wybranych modeli (np. DeepSeek-V3-0324, Kimi-K2-Instruct-0905).
#### Wady i ograniczenia
- Brak spójności w formacie wyjścia między modelami i między zapytaniami.
- Priorytety nie zawsze są stabilne – różnice o 1–2 punkty, czasem większe przy synonimach.
- Nie wszystkie modele uwzględniają pełny zakres pól w rozbudowanej bazie danych.
- Trudności w porównaniu wyników między modelami wymagają dodatkowej normalizacji danych.
#### Finalny wniosek
- Największe trudności pojawiły się w porównywaniu formatów odpowiedzi i stabilności priorytetów.
- Modele DeepSeek-V3-0324 i Kimi-K2-Instruct-0905 sprawowały się najlepiej – trafnie identyfikowały pola i zachowywały względną spójność.
- Modele meta-llama, CohereLabs i inclusionAI były mniej stabilne, miały niepełne pokrycie pól i niestabilne priorytety.
- Zastanawiające jest, czy testy były odpowiednio dopasowane do użytej bazy danych – bardziej ustrukturyzowana baza mogłaby pozwolić na jednoznaczną ocenę modeli.
- Kolejne kroki obejmują testy na większej, ustrukturyzowanej bazie danych w celu sprawdzenia powtarzalności wyników i porównania spójności modeli przy różnych kwerendach.