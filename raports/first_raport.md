# Raport 1 - sprawdzanie potencjału rozwiązania

Pierwszy test
**25.10.2025**

## 1. Cel testu

Celem testu było sprawdzenie, jak różne modele AI interpretują to samo zapytanie użytkownika oraz czy potrafią poprawnie wyłonić najtańsze oferty z tej samej bazy danych JSON.  
  

## 2. Wyniki dla wybranych modeli
  
### Model: DeepSeek-AI
```python
  { "id": 1, "data": "Tylko u nas znajdziesz trekkingowe Mammuty 250zł na www.tanio.pl" },\
  { "id": 6, "data": "Sandały turystyczne Teva w super cenie 180 PLN - sprawdź na mountain-gear.pl" },\
  { "id": 5, "data": "PROMOCJA! Buty trekkingowe Merrell Moab 2 tylko 320zł - oferta ważna do końca miesiąca" },\
  { "id": 4, "data": "Salomon Speedcross 5 GTX - 489 zł | Darmowa dostawa" },\
  { "id": 0, "data": "Buty sportowe La Sportiva 550zł" },\
  { "id": 8, "data": "Adidas Terrex Free Hiker GTX, cena: 599,99zł" }
```
### Model: Moonshot AI
```python
  { "id": 6, "data": "Sandały turystyczne Teva w super cenie 180 PLN" },\
  { "id": 1, "data": "Trekkingowe Mammuty 250zł" },\
  { "id": 5, "data": "Merrell Moab 2 tylko 320zł" },\
  { "id": 0, "data": "La Sportiva 550zł" },\
  { "id": 4, "data": "Salomon Speedcross 5 GTX - 489 zł" },\
  { "id": 8, "data": "Adidas Terrex Free Hiker GTX 599,99zł" }
```
### Model: Meta AI

Model przeprowadził szczegółową analizę danych, wyodrębnił ceny z tekstu i zaproponował algorytm w Pythonie do ich ekstrakcji i porównania.

Najtańsze wykryte produkty:
 - Sandały Teva – 180 PLN
 - Mmuty – 250 zł
 - Mrell Moab 2 – 320 zł

Model poprawnie zidentyfikował najniższą cenę, ale pominął rekordy bez cen.

### Model: OpenAI
```python
  { "id": 6, "data": "Sandały turystyczne Teva w super cenie 180 PLN" },\
  { "id": 1, "data": "Trekkingowe Mammuty 250zł" },\
  { "id": 5, "data": "Merrell Moab 2 tylko 320zł" },\
  { "id": 4, "data": "Salomon Speedcross 5 GTX - 489 zł" },\
  { "id": 0, "data": "La Sportiva 550zł" },\
  { "id": 8, "data": "Adidas Terrex Free Hiker GTX 599,99zł" },\
  { "id": 2, "data": "Poradnik wyboru butów" },\
  { "id": 3, "data": "" },\
  { "id": 7, "data": "Recenzja butów Columbia Redmond" }
```
### Model: InclusionAI

Model jasno określił priorytet: najniższa cena, a następnie poprawnie posortował produkty:
1.	180 PLN – Teva
2.  250 zł – Mammuty
3.	320 zł – Merrell
4.	489 zł – Salomon
5.	550 zł – La Sportiva
6.	599,99 zł – Adidas

Zwrócono wyłącznie rekordy zawierające ceny.

## 3. Analiza wyników

### Najlepsze modele

### 1. Meta AI
Zalety
 - Bardzo szczegółowa analiza
 - Implementacja algorytmu ekstrakcji cen
 - Poprawna identyfikacja najtańszych produktów
 - Wyjaśnienie problemów z kodowaniem znaków

Wady
 - Pominięcie rekordów bez cen

### 2. OpenAI
Zalety
 - lepsze zrozumienie kontekstu zapytania
 - Urządkowanie wszystkich rekordów
 - Rróżnienie produktów i treści informacyjnych
 - Uględnienie różnych walut (PLN = zł)

Wady
 - Brak szczegółowej metodologii
 - Problemy z kodowaniem znaków

### Dobre modele

### 3. InclusionAI
Zalety
 - Czysta i logiczna odpowiedź
 - Poprawna kolejność cen
 - Dobrze sformatowany JSON

Wady
 - Pominięcie rekordów bez cen
 - Brak głębszej analizy

### 4. DeepSeek
Zalety
 - Poprawna struktura JSON
 - Dobra selekcja produktów

Wady
 - Brak jednoznacznego sortowania po cenie
 - Ograniczona analiza

### Słabsze modele

### 5. Moonshot AI
 - Brak analizy
 - Brak sortowania po cenie
 - Pominięcie części rekordów

### 6. Cohere Labs
 - Brak analizy
 - Brak sortowania po cenie
 - Problemy z formatem odpowiedzi