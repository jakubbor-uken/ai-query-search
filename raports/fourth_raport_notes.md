
# ##########
#          #
# RAPORT 4 #
#          #
# ##########

W kolejnej fazie badań...

Do wyników testów dodaliśmy zapisywanie czasu wykonania części kodu odpowiadającej za zapytanie do API modelów huggingface w sekundach, z zaokrągleniem do 3 miejsc po przecinku
elapsed_time = round(end - start, 3)  # rounds to 3 decimal places (0.001 precision)

Rozpoczęliśmy badania na docelowej bazie danych.
Zdecydowaliśmy się również zbadać koszta użycia modelów i określić realność takiego rozwiązania.
Wzięliśmy pod uwagę też czas wykonania zapytań do API



# #########
#  TESTY  #
# #########

Wybraliśmy bazę danych "sampledb.json", zawierającą informacje o dziełach artystów.

# Struktura bazy danych:

inventorynumber - unikalny numer inwentarzowy (np. "MHF 54750/F/90")
createdate - data lub okres powstania dzieła (np. "1915", "1920-1930")
name - tytuł/opis fotografii
size - wymiary w centymetrach (np. "4,1 x 6,5 cm")
material - materiał nośnika (papier, szkło, tektura)
technique - technika fotograficzna (fot. czarno-biała, fot. żelatynowo-srebrowa)
place - miejsce powstania (Polska, Niemcy, Egipt, itd.)
type - rodzaj obiektu (fotografia-pozytyw, diapozytyw)
copyright - status praw autorskich (domena publiczna, prawa nieustalone, MuFo licencjobiorcą)
creator - autor fotografii (lub "nieznany")

Zawartość kolekcji:
Baza zawiera zróżnicowane fotografie:

Portrety osób (historyczne, z lat 1887-1934)
Fotografie wojenne (I Wojna Światowa - Wielka Wojna)
Pejzaże i architektura (Polska, Egipt, Włochy, Szwajcaria)
Sceny życia codziennego
Fotografie sportowe




Przykład losowo wybranego obiektu z bazy danych:
```
{
        "inventorynumber": "MHF 53549/F/14",
        "createdate": "Lata 60. XX w.",
        "name": "Para idąca chodnikiem w deszczu",
        "size": "24,0 x 19,2 cm",
        "material": "papier światłoczuły",
        "technique": "fot. czarno-biała",
        "place": "Polska",
        "type": "fotografia-pozytyw",
        "copyright": "MuFo licencjobiorcą",
        "creator": "Chromiński Witold"
}
```


Do badań zdecydowaliśmy się losowo podzielić bazę danych na kilka części zawierających losowo wybrane elementy (skrypt utilities/random_db_splitter.py)
Bazy danych zawierały następująco: 50, 100, 200, 500 i 959 obiektów i zawarte zostały w plikach:
databases/sampledb50.json
databases/sampledb100.json
databases/sampledb200.json
databases/sampledb500.json
databases/sampledb.json



Aby ułatwić skonstruowanie kwerend o odpowiedniej trudności, wykorzystaliśmy skrypt listujący wszystkie unikalne wartości w bazie danych dla każdej z cech:
`utilities/unique_db_values.py`

Wyniki skryptu zostały zapisane w pliku:
`utilities/unique_values.json`


Wykonaliśmy testy modelów na trzech kwerendach o różnej trudności ustalenia priorytetów cech. Trudność kwerendy została wyjaśniona w poszczególnych podsumowaniach dla każdej z nich.
# //TODO: rozpisać trzy kwerendy na których były prowadzone badania i ich zróżnicowanie w trudności odpowiedzi
Kwerenda zaawansowana: 
> "Znajdź dzieła wykonane w trakcie wojny w danym państwie"
Kwerenda średniozaawansowana: 
> "Znajdź dzieła które są łatwopalne"
Kwerenda trywialna: 
> "Znajdź dzieła przedstawiające ludzi"

Kwerenda dodatkowa pozostała bez zmian od poprzednich testów:
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól (object properties) danych które najbardziej jej odpowiadają i zwróć tylko jeden obiekt wszystkich pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue, \"propertyName\": priorityValue} - odpowiedź musi zawrzeć się tylko w jednym obiekcie, wartości priorytetów mogą być tylko z zakresu od 0 do 100 włącznie, dane podane są poniżej: ###\n"


Do testów wykorzystaliśmy 5 modeli:
`deepseek-ai/DeepSeek-V3-0324`
`moonshotai/Kimi-K2-Instruct-0905`
`openai/gpt-oss-20b:groq`
`CohereLabs/command-a-translate-08-2025:cohere`
`inclusionAI/Ling-1T:featherless-ai`



Testy dla każdej bazy danych powtórzyliśmy 3 razy.




Problemy:
W trakcie wykonania próbnego napotkaliśmy problem z modelem:
> CohereLabs/command-a-translate-08-2025:cohere

```
openai.BadRequestError: Error code: 400 - {'id': 'ef1ad312-576b-4720-8cd4-4b1759942dac', 'message': 'too many tokens: size limit exceeded by 105000 tokens. Try using shorter or fewer inputs. The limit for this model is 8992 tokens.'}
```

Limit tokenów w jednej wiadomości został znacznie przekroczony.
W związku z tym zedytowaliśmy kod źródłowy i przeprowadziliśmy badania dla tego modelu tylko na bazie danych zawierającej 50 obiektów ("sampledb50.json")



jak również z modelem 
> "inclusionAI/Ling-1T:featherless-ai"

```
2025-11-24 22:02:35 | INFO | _client.py:1025 >>> HTTP Request: POST https://router.huggingface.co/v1/chat/completions "HTTP/1.1 503 Service Temporarily Unavailable"
```

który odrzucał za pytania, najprawdopodobniej ze względu na przekroczenie limitu input tokenów

na temat modelu znaleźliśmy informację:
`Pre-trained on 20 trillion+ high-quality, reasoning-dense tokens, Ling-1T-base supports up to 128K context length`
która sugerowała by że na bazie danych `sampledb500.json` model wciąż powinien być w stanie wykonać kwerendę (miała ona 67300 tokenów), jednak api odrzucało zapytanie z kodem błędu HTTP 503 przy próbie wysłania bazy danych - prawdopodobnie 128K contextu oznaczało 64K inputu i 64K outputu. W związku z tym również został pominięty w testach powyżej 200 obiektów.




Wyniki testów:



# ----------------------------------
# | TEST 1 - KWERENDA ZAAWANSOWANA |
# ----------------------------------

Test pierwszy - zaawansowana kwerenda
"query": "Znajdź dzieła wykonane w trakcie wojny w danym państwie"

# Dlaczego ta kwerenda jest zaawansowana?

1. Wymaga połączenia wielu cech z bazy danych
Aby odpowiedzieć na to zapytanie, system musi analizować i łączyć informacje z kilku pól:

createdate - data powstania dzieła
place - lokalizacja powstania
name - tytuł/opis dzieła (często zawiera kontekst historyczny)
creator - autor (może pomóc w datowaniu)


2. Nie jest zapytaniem wprost (brak bezpośredniego pola)
Baza danych nie zawiera dedykowanego pola typu:

`war: true/false`
`conflict: "I Wojna Światowa"`
`wartime_context: "military operation"`


Informacje o kontekście wojennym są rozprószone i trzeba je wnioskować z różnych źródeł.
3. Wymaga wiedzy zewnętrznej (poza bazą danych)
        A) Wiedza historyczna o konfliktach
        B) Wiedza geograficzna
        C) Wiedza o chronologii


4. Wymaga analizy semantycznej tytułów


5. Wymaga rozpoznawania sygnałów wojennych
Silne sygnały:

Słowa kluczowe: "wojna", "artyleria", "żołnierz", "front", "atak"
Tytuły wojskowe: "rotmistrz", "kapitan"
Obiekty militarne: "amunicja", "działon", "okopy"
Zniszczenia: "ruiny", "zrujnowany ogniem"

Średnie sygnały:

Data w trakcie znanego konfliktu
Miejsce będące frontem
Kontekst uchodźców: "uciekinierzy z Prus Wschodnich"

Słabe sygnały:

Sam fakt istnienia w okresie wojny (życie cywilne toczyło się dalej)
Obecność munduru (może być zdjęcie portretowe w czasie pokoju)


6. Niejednoznaczność i niepewność
Problem 1: Granice czasowe
createdate: "1915-1941"  # Czy to wojenne? 
→ Zakres obejmuje okres wojenny I WŚ (1914-1918)
→ ALE TAKŻE okres międzywojenny (1919-1938)
→ I początek II WŚ (1939-1941)
→ Nie można jednoznacznie stwierdzić bez dodatkowego kontekstu

Problem 2: Nieścisłe datowanie
createdate: "ok. 1900"
→ Przed I WŚ, prawdopodobnie pokojowe
→ ALE "ok." oznacza niepewność ±5-10 lat?

createdate: "1890-1916"
→ Koniec zakresu pokrywa się z I WŚ
→ Czy zdjęcie powstało w 1890 czy 1916?

Problem 3: Lokalizacja vs. tematyka
{
  "place": "Polska",
  "createdate": "1915",
  "name": "Kobieta w pokoju werandowym"
}
→ Data i miejsce: potencjalnie wojenne
→ Tematyka: wyraźnie cywilna, portret prywatny
→ WNIOSEK: Prawdopodobnie NIE jest związane z wojną


7. Przykładowe przypadki graniczne
Przypadek A: Wysoka pewność ✓
{
  "name": "Wielka Wojna, atak niemieckiej piechoty pod Reims",
  "createdate": "1918-1941",
  "place": "Francja"
}
→ JEDNOZNACZNIE wojenne (I WŚ, Francja, jawna tematyka)


Przypadek B: Średnia pewność ~
{
  "name": "Wieliczka, zniszczenia wojenne wizytowane przez księcia biskupa",
  "createdate": "2 stycznia 1915",
  "place": "Polska"
}
→ PRAWDOPODOBNIE wojenne (data pasuje, zniszczenia + "wojenne" w tytule)


Przypadek C: Niska pewność ?
{
  "name": "Mężczyzna, portret",
  "createdate": "1920-1930",
  "place": "nieznane"
}
→ TRUDNO STWIERDZIĆ (okres po I WŚ, ale brak kontekstu)


Przypadek D: Wymaga wiedzy specjalistycznej ⚠️
{
  "name": "Wilno, I Ogólnopolskie Zawody Sportowe...",
  "createdate": "styczeń 1934",
  "place": "Litwa"
}
→ Miejsce: dziś Litwa, ale w 1934 było polskie
→ Czas: okres międzywojenny (pokój)
→ Tematyka: sport (cywilna)
→ WNIOSEK: NIE wojenne







Pierwotnie założyliśmy następujące wartości priorytetów dla tej kwerendy:
{
        "inventorynumber": 0
        "createdate": 100
        "name": 70
        "size": 0
        "material": 0
        "technique": 20
        "place": 100
        "type": 20
        "copyright": 0
        "creator": 70
},

Jednak ze względu na problemy badawcze w określeniu jednoznacznego priorytetu, zdecydowaliśmy się po prostu odesparować dane które są adekwatne do kwerendy:
Adektwane: ["createdate", "place", "name", "creator"]
Wyjaśnienie naszego toku myślenia:
createdate - zawiera rok lub przedział lat w których obraz został wykonany, w połączeniu z "place" pozwala określić czy trwał konflikt zbrojny w tym kraju
place - zawiera miejsce wykonania, w połączeniu z  w połączeniu z "createdate" pozwala określić czy trwał konflikt zbrojny w tym kraju
name - tytuł dzieła sugeruje jego tematykę, można określić czy to tematyka wojenna - jeżeli tak, większe prawdopodobieństwo że trwał konflikt zbrojny
creator - imię i nazwisko autora, pozwala określić w jakich latach żył, skąd jest itp. i na podstawie tego określić czy mógł wtedy trwać konflikt zbrojny

Pozostałe cechy nie zapewniały źródeł informacji wysokiej jakości w kontekście kwerendy, w związku z tym nie zostały uwzględnione w najważniejszych cechach 


Przy określaniu rzetelności modelu stwierdziliśmy że nie można jednoznacznie ustalić jaki dokładny priorytet będzie miała dana cecha, bo określenie która cecha ma jak duże znaczenie wymaga subiektywności,
ale można określić które priorytety będą miały największe znaczenie w kontekście danej kwerendy. 
Ze względu na to, że program najczęściej będzie wykorzystywany do filtracji bazy danych, założyliśmy że musimy ustalić jakiś próg który określi adekwatne cechy.
W związku z tym badamy tylko:
- czy adekwatne cechy miały priorytet >= 50.
- czy wszystkie adekwatne cechy były zawarte w 4 najwyższych priorytetach 
- czy względny rozkład priorytetów się zgadzał w obrębie tego samego modelu i jeśli nie, to jak duża była rozbieżność 
# //TODO: SPRAWDZIĆ JAKOŚ STATYSTYCZNIE CZY ROZKŁAD SIĘ ZGADZAŁ I JAKA BYŁA ROZBIEŻNOŚĆ


Dla każdego rozmiaru bazy danych wykonaliśmy testy trzykrotnie.
Jeżeli miały, to zakładamy że model określił priorytety poprawnie.


### Pierwszy test na bazie danych o ilości obiektów 50:

{'output': {'createdate': 90, 'name': 80, 'place': 70, 'type': 60, 'material': 50, 'technique': 40, 'size': 30, 'creator': 20, 'copyright': 10, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 4.428}
{'output': {'name': 100, 'createdate': 95, 'place': 90, 'inventorynumber': 30, 'type': 25, 'material': 20, 'technique': 15, 'size': 10, 'copyright': 5, 'creator': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 0.632}
{'output': {'createdate': 90, 'place': 80, 'type': 70}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.196}
{'output': {'createdate': 100, 'name': 100, 'place': 100, 'technique': 100}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 2.044}
{'output': {'place': 100, 'createdate': 95, 'name': 90, 'technique': 70, 'type': 60, 'material': 50, 'size': 40, 'creator': 30, 'copyright': 10, 'inventorynumber': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 8.394}

## Drugi test na bazie danych o ilości obiektów 50:

{'output': {'createdate': 90, 'name': 80, 'place': 70, 'creator': 60, 'type': 50, 'material': 40, 'technique': 30, 'size': 20, 'copyright': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 3.447}
{'output': {'name': 100, 'createdate': 95, 'place': 90, 'inventorynumber': 85, 'type': 80, 'material': 75, 'technique': 70, 'size': 65, 'copyright': 60, 'creator': 55}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 0.997}
{'output': {'inventorynumber': 20, 'createdate': 90, 'name': 80, 'size': 20, 'material': 20, 'technique': 20, 'place': 100, 'type': 20, 'copyright': 20, 'creator': 20}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.461}
{'output': {'createdate': 100, 'name': 100, 'place': 100, 'inventorynumber': 50, 'material': 50, 'technique': 50, 'type': 50, 'copyright': 50, 'creator': 50, 'size': 0}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 2.98}
{'output': {'place': 100, 'createdate': 100, 'name': 100, 'type': 90, 'technique': 80, 'material': 70, 'creator': 60, 'size': 50, 'copyright': 10, 'inventorynumber': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 7.805}


# Trzeci test na bazie danych o ilości obiektów 50:

{'output': {'createdate': 90, 'name': 80, 'place': 70, 'type': 60, 'material': 50, 'technique': 40, 'size': 30, 'creator': 20, 'copyright': 10, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 3.265}
{'output': {'name': 100, 'createdate': 95, 'place': 90, 'inventorynumber': 85, 'type': 80, 'technique': 75, 'material': 70, 'size': 65, 'copyright': 60, 'creator': 55}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 0.716}
{'output': {'inventorynumber': 20, 'createdate': 90, 'name': 75, 'size': 25, 'material': 30, 'technique': 40, 'place': 85, 'type': 80, 'copyright': 10, 'creator': 20}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.128}
{'output': {'createdate': 100, 'name': 100, 'place': 100, 'inventorynumber': 50, 'material': 50, 'technique': 50, 'type': 50, 'copyright': 50, 'creator': 50, 'size': 0}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 2.247}
{'output': {'place': 100, 'createdate': 100, 'name': 100, 'type': 90, 'technique': 70, 'material': 60, 'size': 50, 'creator': 40, 'copyright': 30, 'inventorynumber': 20}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 8.295}




# Podsumowanie testu na bazie danych o ilości obiektów 50:
# //TODO PODSUMOWANIE




!!!
Pominięto testy na modelu CohereLabs/command-a-translate-08-2025:cohere na większych bazach danych
ze względu na problemy z limitem kontekstu wspomiane na początku raportu.
!!!

### Pierwszy test na bazie danych o ilości obiektów 100:

{'output': {'createdate': 100, 'name': 90, 'place': 80, 'type': 70, 'material': 60, 'technique': 50, 'creator': 40, 'copyright': 30, 'size': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 3.667}
{'output': {'createdate': 100, 'name': 90, 'place': 80, 'type': 70, 'technique': 60, 'material': 50, 'creator': 40, 'size': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.632}
{'output': {'place': 100, 'createdate': 90, 'type': 70, 'name': 50, 'material': 40, 'technique': 40, 'inventorynumber': 30, 'creator': 30, 'copyright': 20}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.945}
{'output': {'createdate': 100, 'place': 100, 'name': 90, 'creator': 70, 'technique': 60, 'material': 50, 'type': 40, 'size': 30, 'inventorynumber': 20, 'copyright': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 8.188}


## Drugi test na bazie danych o ilości obiektów 100:

{'output': {'createdate': 100, 'place': 90, 'name': 80, 'type': 70, 'material': 60, 'technique': 50, 'size': 40, 'creator': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 4.135}
{'output': {'inventorynumber': 100, 'createdate': 100, 'name': 95, 'place': 90, 'type': 85, 'material': 70, 'technique': 70, 'copyright': 60, 'creator': 55, 'size': 50}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 7.298}
{'output': {'createdate': 100, 'place': 95, 'name': 85, 'type': 80, 'creator': 75, 'material': 70, 'technique': 65, 'size': 60, 'copyright': 55, 'inventorynumber': 50}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 2.132}
{'output': {'createdate': 100, 'place': 100, 'name': 85, 'creator': 70, 'technique': 60, 'material': 50, 'type': 40, 'size': 30, 'inventorynumber': 20, 'copyright': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 6.837}


# Trzeci test na bazie danych o ilości obiektów 100:

{'output': {'createdate': 90, 'name': 80, 'place': 70, 'type': 60, 'material': 50, 'technique': 40, 'creator': 30, 'copyright': 20, 'size': 10, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 3.698}
{'output': {'inventorynumber': 100, 'createdate': 100, 'name': 95, 'place': 90, 'type': 85, 'technique': 80, 'material': 75, 'copyright': 70, 'creator': 65, 'size': 60}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 0.72}
{'output': {'inventorynumber': 10, 'createdate': 100, 'name': 70, 'size': 5, 'material': 20, 'technique': 20, 'place': 90, 'type': 60, 'copyright': 0, 'creator': 50}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.948}
{'output': {'createdate': 100, 'place': 80, 'name': 70, 'creator': 60, 'technique': 50, 'type': 40, 'material': 30, 'size': 20, 'inventorynumber': 10, 'copyright': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 9.203}


# Podsumowanie testu na bazie danych o ilości obiektów 100:

# //TODO PODSUMOWANIE





### Pierwszy test na bazie danych o ilości obiektów 200:

{'output': {'createdate': 90, 'place': 80, 'name': 70, 'creator': 60, 'type': 50, 'technique': 40, 'material': 30, 'size': 20, 'copyright': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 5.898}
{'output': {'inventorynumber': 100, 'createdate': 100, 'name': 90, 'place': 100, 'type': 80, 'material': 60, 'technique': 60, 'copyright': 60, 'creator': 60, 'size': 40}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 3.599}
{'output': {'inventorynumber': 5, 'createdate': 95, 'name': 70, 'size': 30, 'material': 20, 'technique': 25, 'place': 100, 'type': 10, 'copyright': 15, 'creator': 60}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 2.562}
{'output': {'place': 100, 'createdate': 90, 'name': 80, 'creator': 70, 'technique': 60, 'material': 50, 'size': 40, 'type': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 10.006}


## Drugi test na bazie danych o ilości obiektów 200:

{'output': {'createdate': 90, 'name': 80, 'place': 70, 'type': 60, 'material': 50, 'technique': 40, 'size': 30, 'creator': 20, 'copyright': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 5.163}
{'output': {'createdate': 100, 'place': 95, 'name': 85, 'inventorynumber': 60, 'material': 30, 'technique': 25, 'size': 20, 'copyright': 15, 'creator': 10, 'type': 5}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.016}
{'output': {'inventorynumber': 20, 'createdate': 100, 'name': 50, 'size': 30, 'material': 30, 'technique': 30, 'place': 100, 'type': 60, 'copyright': 20, 'creator': 40}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 3.078}
{'output': {'createdate': 100, 'place': 100, 'name': 90, 'creator': 70, 'technique': 60, 'material': 50, 'size': 40, 'type': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 6.774}


# Trzeci test na bazie danych o ilości obiektów 200:

{'output': {'createdate': 90, 'place': 80, 'name': 70, 'type': 60, 'material': 50, 'technique': 40, 'creator': 30, 'copyright': 20, 'size': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 5.676}
{'output': {'createdate': 100, 'name': 90, 'place': 80, 'inventorynumber': 70, 'type': 60, 'technique': 50, 'material': 40, 'size': 30, 'copyright': 20, 'creator': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 2.587}
{'output': {'inventorynumber': 20, 'createdate': 90, 'name': 70, 'size': 30, 'material': 35, 'technique': 40, 'place': 100, 'type': 80, 'copyright': 15, 'creator': 50}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 2.308}
{'output': {'place': 100, 'createdate': 90, 'name': 85, 'creator': 70, 'technique': 60, 'material': 50, 'size': 40, 'type': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 11.142}


# Podsumowanie testu na bazie danych o ilości obiektów 200:

# //TODO PODSUMOWANIE


!!!
Pominięto testy na modelu "inclusionAI/Ling-1T:featherless-ai" na bazach danych powyżej 200 obiektów
ze względu na problemy z limitem kontekstu wspomiane na początku raportu.
!!!


### Pierwszy test na bazie danych o ilości obiektów 500:

{'output': {'createdate': 90, 'place': 80, 'name': 70, 'creator': 60, 'inventorynumber': 50, 'type': 40, 'material': 30, 'technique': 20, 'size': 10, 'copyright': 5}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 11.605}
{'output': {'createdate': 100, 'place': 95, 'name': 90, 'inventorynumber': 85, 'type': 80, 'technique': 75, 'material': 70, 'size': 65, 'copyright': 60, 'creator': 55}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.296}
{'output': {'createdate': 95, 'place': 90, 'type': 70, 'name': 45, 'creator': 35, 'material': 25, 'technique': 25, 'size': 20, 'copyright': 10, 'inventorynumber': 5}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 5.632}


## Drugi test na bazie danych o ilości obiektów 500:

{'output': {'createdate': 90, 'place': 80, 'name': 70, 'type': 60, 'material': 50, 'technique': 40, 'creator': 30, 'size': 20, 'copyright': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 13.038}
{'output': {'createdate': 100, 'place': 95, 'name': 90, 'technique': 85, 'type': 80, 'material': 75, 'size': 70, 'creator': 65, 'copyright': 60, 'inventorynumber': 55}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.201}
{'output': {'inventorynumber': 10, 'createdate': 100, 'name': 60, 'size': 30, 'material': 40, 'technique': 30, 'place': 90, 'type': 50, 'copyright': 20, 'creator': 30}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 4.818}


# Trzeci test na bazie danych o ilości obiektów 500:

{'output': {'createdate': 100, 'place': 90, 'name': 80, 'type': 70, 'material': 60, 'technique': 50, 'creator': 40, 'size': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 9.049}
{'output': {'createdate': 100, 'place': 95, 'name': 90, 'inventorynumber': 85, 'type': 80, 'technique': 75, 'material': 70, 'size': 65, 'copyright': 60, 'creator': 55}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.126}
{'output': {'inventorynumber': 5, 'createdate': 90, 'name': 10, 'size': 10, 'material': 20, 'technique': 20, 'place': 100, 'type': 50, 'copyright': 5, 'creator': 20}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 2.15}


# Podsumowanie testu na bazie danych o ilości obiektów 500:

# //TODO PODSUMOWANIE






### Pierwszy test na bazie danych o ilości obiektów 959:

{'output': {'createdate': 100, 'place': 90, 'name': 80, 'type': 70, 'material': 60, 'technique': 50, 'size': 40, 'copyright': 30, 'creator': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 40.889}
{'output': {'createdate': 100, 'place': 90, 'name': 80, 'type': 70, 'technique': 60, 'material': 50, 'size': 40, 'creator': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 9.366}
{'output': {'place': 100, 'createdate': 90, 'type': 80, 'name': 60, 'creator': 40, 'material': 20, 'technique': 20, 'copyright': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 8.583}


## Drugi test na bazie danych o ilości obiektów 959:

{'output': {'createdate': 100, 'place': 90, 'name': 80, 'type': 70, 'material': 60, 'technique': 50, 'size': 40, 'copyright': 30, 'creator': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 37.133}
{'output': {'createdate': 100, 'place': 80, 'name': 60, 'inventorynumber': 40, 'creator': 20, 'material': 10, 'technique': 10, 'size': 5, 'copyright': 5, 'type': 5}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 10.533}
{'output': {'createdate': 100, 'place': 95, 'type': 20, 'name': 15, 'material': 5, 'technique': 5, 'size': 5, 'creator': 5, 'inventorynumber': 0, 'copyright': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 7.57}


# Trzeci test na bazie danych o ilości obiektów 959:

{'output': {'createdate': 100, 'place': 90, 'name': 80, 'type': 70, 'material': 60, 'technique': 50, 'size': 40, 'copyright': 30, 'creator': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 8.405}
{'output': {'createdate': 100, 'place': 95, 'name': 90, 'type': 85, 'technique': 80, 'material': 75, 'creator': 70, 'copyright': 65, 'size': 60, 'inventorynumber': 55}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 1.594}
{'output': {'createdate': 90, 'place': 80, 'name': 70, 'type': 60, 'creator': 50, 'material': 40, 'technique': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła wykonane w trakcie wojny w danym państwie', 'elapsed_time': 7.311}


# Podsumowanie testu na bazie danych o ilości obiektów 959:

# //TODO PODSUMOWANIE








### Podsumowanie wszystkich testów kwerendy zaawansowanej:
# //TODO PODSUMOWANIE













# -----------------------------------------
# | TEST 2 - KWERENDA ŚREDNIOZAAWANSOWANA |
# -----------------------------------------

Test drugi - średniozaawansowana kwerenda
"query": "Znajdź dzieła które są łatwopalne"

# Dlaczego ta kwerenda jest średniozaawansowana?

1. Wymaga połączenia i interpretacji cech
Zapytanie odnosi się do właściwości fizycznych materiału, ale baza zawiera jedynie:

`material` - nazwa materiału (np. "papier", "szkło", "tektura")
`technique` - technika wykonania (np. "fot. czarno-biała")
Nie ma bezpośredniego pola typu `flammable: true/false` lub `fire_risk: "high"`

2. Wymaga wiedzy zewnętrznej o właściwościach materiałów
System musi "wiedzieć" które materiały są łatwopalne

3. Analiza z bazy danych
> Z przykładowych 49 rekordów:
Rozkład materiałów:
- papier: 30 rekordów (61%)
- papier światłoczuły: 13 rekordów (27%)
- szkło: 5 rekordów (10%)
- tektura: 1 rekord (2%)

ŁATWOPALNE (papier + papier światłoczuły + tektura): 44/49 = 90%
NIEPALNE (szkło): 5/49 = 10%


4. Przypadki wymagające uwagi
A) Niejednoznaczne nazwy materiałów

```
{
  "material": "papier",  // OK, jasne
}

{
  "material": "papier światłoczuły",  // Czym się różni od zwykłego papieru?
  // Odpowiedź: Zawiera światłoczułe substancje chemiczne
  // Może być BARDZIEJ łatwopalny ze względu na chemikalia
}
```


B) Brak informacji o obróbce

```
{
  "material": "papier",
  // Czy był zabezpieczony? Laminowany? Zalany w szkle?
  // Baza nie zawiera informacji o dodatkowej ochronie
}
```

C) Materiały kompozytowe (gdyby wystąpiły)
```
"papier na tekturze" → jak ocenić?
"fotografia w ramie szklanej" → sama fotografia łatwopalna, ale chroniona
```


5. Dlaczego to ŚREDNIO-, a nie wysoko-zaawansowana?
Prostsze niż Test 1, bo:

✓ Wymaga analizy jednego pola (material), nie wielu
✓ Mapowanie jest deterministyczne (papier = łatwopalny), nie probabilistyczne
✓ Nie wymaga analizy kontekstu historycznego ani dat
✓ Wiedza zewnętrzna jest prosta (właściwości fizyczne) i stabilna (nie zmienia się w czasie)

Bardziej złożone niż zapytanie proste, bo:

✗ Nie jest zapytaniem wprost (brak pola flammable)
✗ Wymaga wiedzy z chemii/fizyki materiałów
✗ Wymaga interpretacji semantycznej ("łatwopalne" → lista materiałów)









Wyjaśnienie naszego toku myślenia:
material - zawiera materiał, czyli konkretnie to o co pytamy (tylko nie wprost, w przeciwieństwie do kwerendy trywialnej)

Pozostałe cechy mogły zawierać informacje pomagające odpowiedzieć na kwerendę, ale żadne z nich nie było aż tak ważne jak pole `material`.


W tej części badań badamy tylko:
- czy pole `material` uzyskało najwyższy priorytet


jeżeli tak, określamy że model odpowiedział poprawnie.






### Pierwszy test na bazie danych o ilości obiektów 50:

{'output': {'material': 100, 'name': 20, 'technique': 10, 'type': 10, 'size': 5, 'place': 5, 'creator': 5, 'copyright': 5, 'createdate': 0, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 3.64}
{'output': {'material': 100, 'type': 90, 'technique': 80, 'name': 70, 'size': 60, 'createdate': 50, 'creator': 40, 'place': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.112}
{'output': {'inventorynumber': 0, 'createdate': 0, 'name': 0, 'size': 0, 'material': 100, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0, 'creator': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.435}
{'output': {'material': 100, 'technique': 100, 'type': 100}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.738}
{'output': {'material': 100, 'technique': 100, 'place': 80, 'creator': 70, 'type': 90, 'size': 30, 'createdate': 60, 'name': 85, 'inventorynumber': 10, 'copyright': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 7.974}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
CohereLabs/command-a-translate-08-2025:cohere - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

## Drugi test na bazie danych o ilości obiektów 50:

{'output': {'material': 100, 'technique': 50, 'type': 30}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 3.065}
{'output': {'material': 100, 'type': 80, 'technique': 60, 'name': 40, 'size': 30, 'createdate': 20, 'inventorynumber': 10, 'place': 5, 'copyright': 5, 'creator': 5}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.228}
{'output': {'inventorynumber': 0, 'createdate': 0, 'name': 0, 'size': 0, 'material': 100, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0, 'creator': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.837}
{'output': {'material': 100, 'technique': 100, 'type': 100}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.229}
{'output': {'material': 100, 'technique': 100, 'place': 100, 'type': 100, 'creator': 0, 'size': 0, 'createdate': 0, 'name': 0, 'inventorynumber': 0, 'copyright': 0}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 7.062}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
CohereLabs/command-a-translate-08-2025:cohere - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE


# Trzeci test na bazie danych o ilości obiektów 50:

{'output': {'material': 100, 'technique': 50, 'type': 30}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 2.993}
{'output': {'material': 100, 'type': 90, 'technique': 80, 'name': 70, 'size': 60, 'createdate': 50, 'place': 40, 'creator': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 0.706}
{'output': {'inventorynumber': 0, 'createdate': 0, 'name': 0, 'size': 0, 'material': 100, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0, 'creator': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.328}
{'output': {'material': 100, 'technique': 100, 'type': 100, 'copyright': 100, 'inventorynumber': 0, 'createdate': 0, 'name': 0, 'size': 0, 'place': 0, 'creator': 0}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 2.769}
{'output': {'material': 100, 'technique': 100, 'type': 100, 'place': 80, 'creator': 50, 'name': 70, 'createdate': 60, 'size': 30, 'inventorynumber': 10, 'copyright': 0}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 8.182}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
CohereLabs/command-a-translate-08-2025:cohere - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE


# Podsumowanie testu na bazie danych o ilości obiektów 50:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `material` uzyskało najwyższy priorytet



!!!
Pominięto testy na modelu CohereLabs/command-a-translate-08-2025:cohere na większych bazach danych
ze względu na problemy z limitem kontekstu wspomiane na początku raportu.
!!!


### Pierwszy test na bazie danych o ilości obiektów 100:

{'output': {'material': 100, 'type': 80, 'technique': 60, 'name': 40, 'place': 20, 'copyright': 10, 'creator': 5}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 3.802}
{'output': {'material': 100, 'technique': 20, 'type': 10, 'size': 5, 'name': 0, 'createdate': 0, 'place': 0, 'creator': 0, 'copyright': 0, 'inventorynumber': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.632}
{'output': {'inventorynumber': 0, 'createdate': 0, 'name': 0, 'size': 0, 'material': 100, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0, 'creator': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 5.113}
{'output': {'material': 100, 'technique': 90, 'place': 85, 'creator': 75, 'createdate': 70, 'type': 65, 'name': 60, 'size': 50, 'inventorynumber': 30, 'copyright': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 7.99}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE


## Drugi test na bazie danych o ilości obiektów 100:

{'output': {'material': 100, 'technique': 50, 'type': 30}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 2.958}
{'output': {'material': 100, 'technique': 0, 'type': 0, 'createdate': 0, 'inventorynumber': 0, 'name': 0, 'size': 0, 'place': 0, 'copyright': 0, 'creator': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.539}
{'output': {'inventorynumber': 0, 'createdate': 0, 'name': 0, 'size': 0, 'material': 100, 'technique': 10, 'place': 0, 'type': 10, 'copyright': 0, 'creator': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.427}
{'output': {'material': 100, 'technique': 80, 'place': 60, 'createdate': 70, 'name': 90}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 7.578}


deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

# Trzeci test na bazie danych o ilości obiektów 100:

{'output': {'material': 90, 'type': 70, 'technique': 50, 'name': 30, 'size': 20, 'place': 10, 'createdate': 5, 'creator': 5, 'copyright': 5, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 3.802}
{'output': {'material': 100, 'type': 80, 'technique': 60, 'size': 40, 'name': 20, 'inventorynumber': 10, 'createdate': 5, 'place': 5, 'copyright': 0, 'creator': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.743}
{'output': {'inventorynumber': 10, 'createdate': 20, 'name': 30, 'size': 10, 'material': 90, 'technique': 70, 'place': 15, 'type': 60, 'copyright': 5, 'creator': 25}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.457}
{'output': {'material': 100, 'technique': 90, 'type': 70, 'place': 50, 'creator': 30, 'size': 20, 'inventorynumber': 10, 'createdate': 5, 'name': 5, 'copyright': 1}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 6.519}


deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

# Podsumowanie testu na bazie danych o ilości obiektów 100:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `material` uzyskało najwyższy priorytet





### Pierwszy test na bazie danych o ilości obiektów 200:

{'output': {'material': 95, 'technique': 30, 'type': 25, 'name': 5, 'place': 5, 'createdate': 5}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 4.517}
{'output': {'material': 100, 'type': 90, 'technique': 80, 'name': 70, 'inventorynumber': 60, 'createdate': 50, 'size': 40, 'place': 30, 'copyright': 20, 'creator': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 2.752}
{'output': {'material': 100, 'inventorynumber': 0, 'createdate': 0, 'name': 0, 'size': 0, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0, 'creator': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 2.458}
{'output': {'material': 100, 'technique': 100, 'place': 90, 'createdate': 80, 'name': 70, 'size': 60, 'type': 50, 'copyright': 30, 'creator': 20, 'inventorynumber': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 10.953}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

## Drugi test na bazie danych o ilości obiektów 200:

{'output': {'material': 100, 'type': 50, 'technique': 30}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 4.108}
{'output': {'material': 100, 'type': 90, 'technique': 80, 'name': 70, 'inventorynumber': 60, 'createdate': 50, 'size': 40, 'place': 30, 'copyright': 20, 'creator': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 3.483}
{'output': {'material': 100, 'technique': 80, 'name': 70, 'inventorynumber': 60, 'size': 50, 'creator': 40, 'place': 30, 'type': 20, 'copyright': 10, 'createdate': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 2.557}
{'output': {'material': 100, 'technique': 100, 'place': 80, 'createdate': 70, 'name': 60, 'size': 50, 'type': 40, 'creator': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 11.358}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

# Trzeci test na bazie danych o ilości obiektów 200:

{'output': {'material': 90, 'technique': 70, 'type': 60, 'name': 30, 'size': 20}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 4.683}
{'output': {'material': 100, 'type': 80, 'technique': 60, 'copyright': 40, 'createdate': 20, 'name': 10, 'creator': 5, 'place': 5, 'size': 0, 'inventorynumber': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.413}
{'output': {'inventorynumber': 10, 'createdate': 30, 'name': 60, 'size': 40, 'material': 100, 'technique': 70, 'place': 50, 'type': 80, 'copyright': 20, 'creator': 70}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 2.559}
{'output': {'material': 100, 'technique': 100, 'place': 80, 'createdate': 60, 'name': 40, 'size': 20, 'type': 20, 'copyright': 10, 'creator': 10, 'inventorynumber': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 7.365}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

# Podsumowanie testu na bazie danych o ilości obiektów 200:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `material` uzyskało najwyższy priorytet


### Pierwszy test na bazie danych o ilości obiektów 500:

{'output': {'material': 100, 'technique': 80, 'type': 60, 'size': 40, 'name': 20}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 8.472}
{'output': {'material': 100, 'type': 80, 'technique': 60, 'size': 40, 'name': 30, 'createdate': 20, 'place': 10, 'creator': 5, 'copyright': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 5.855}
{'output': {'inventorynumber': 5, 'createdate': 5, 'name': 30, 'size': 20, 'material': 100, 'technique': 80, 'place': 60, 'type': 95, 'copyright': 5, 'creator': 40}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 5.295}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE

## Drugi test na bazie danych o ilości obiektów 500:

{'output': {'material': 90, 'technique': 70, 'type': 60, 'name': 30, 'createdate': 20, 'size': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 9.152}
{'output': {'material': 100, 'type': 90, 'technique': 80, 'name': 70, 'size': 60, 'createdate': 50, 'creator': 40, 'place': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 5.639}
{'output': {'material': 100, 'type': 80, 'name': 70, 'createdate': 60, 'place': 50, 'inventorynumber': 40, 'size': 30, 'technique': 20, 'copyright': 10, 'creator': 10}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 2.538}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE

# Trzeci test na bazie danych o ilości obiektów 500:

{'output': {'material': 90, 'technique': 70, 'type': 50}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 13.834}
{'output': {'material': 100, 'type': 90, 'technique': 80, 'name': 70, 'size': 60, 'createdate': 50, 'creator': 40, 'place': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.201}
{'output': {'inventorynumber': 5, 'createdate': 10, 'name': 20, 'size': 10, 'material': 100, 'technique': 80, 'place': 10, 'type': 70, 'copyright': 5, 'creator': 15}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 5.63}


deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE

# Podsumowanie testu na bazie danych o ilości obiektów 500:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `material` uzyskało najwyższy priorytet




### Pierwszy test na bazie danych o ilości obiektów 959:

{'output': {'material': 100, 'technique': 80, 'type': 60, 'name': 40, 'size': 20}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 37.506}
{'output': {'material': 100, 'technique': 90, 'type': 80, 'name': 70, 'size': 60, 'createdate': 50, 'place': 40, 'creator': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 9.301}
{'output': {'inventorynumber': 0, 'createdate': 0, 'name': 0, 'size': 0, 'material': 100, 'technique': 0, 'place': 0, 'type': 80, 'copyright': 0, 'creator': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 8.188}


deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE


## Drugi test na bazie danych o ilości obiektów 959:

{'output': {'material': 100, 'technique': 80, 'type': 60, 'name': 40, 'size': 20}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 36.697}
{'output': {'material': 100, 'type': 90, 'technique': 80, 'name': 70, 'size': 60, 'createdate': 50, 'place': 40, 'creator': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.516}
{'output': {'material': 100, 'technique': 80, 'type': 60, 'creator': 20, 'name': 10, 'place': 10, 'createdate': 10, 'inventorynumber': 5}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 7.589}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE


# Trzeci test na bazie danych o ilości obiektów 959:

{'output': {'material': 100, 'technique': 80, 'type': 60, 'size': 40, 'name': 20}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 11.592}
{'output': {'material': 100, 'type': 90, 'technique': 80, 'name': 70, 'size': 60, 'createdate': 50, 'place': 40, 'creator': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 1.344}
{'output': {'material': 100, 'type': 0, 'createdate': 0, 'inventorynumber': 0, 'name': 0, 'size': 0, 'technique': 0, 'place': 0, 'copyright': 0, 'creator': 0}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła które są łatwopalne', 'elapsed_time': 7.754}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE


# Podsumowanie testu na bazie danych o ilości obiektów 959:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `material` uzyskało najwyższy priorytet









# TODO: napisać czym się różniły priorytety reszty cech i czy to ma jakiekolwiek znaczenie przy tej kwerendzie (nie - bo otrzymaliśmy najważniejszy priorytet jako najwyższy, tak - bo niektóre modele zwracały inne cechy z wysokim priorytetem, a inne te same cechy z niskim, w związku z tym przy filtracji i źle dopasowanych progach brania pod uwagę priorytetów mogło by to wpłynąć na efektywność dalszego przeszukiwania, napisać o kolejności cech w outpucie i że to nie ma znaczenia bo kolejność cech nie powinna wpływać na to jak obiekt będzie traktowany w kodzie przy próbie dalszego wykorzystania wyników, zastanowić się nad rozbieżnością w określaniu priorytetów w różnych modelach, niektóre ustalały wszystkie inne na 0, niektóre rozkładały je w inny sposób, zapisać wnioski o zachowaniu danego modelu w wypadku priorytetów które mają niskie znaczenie i że rozkład priorytetów naszym zdaniem u poszczególnych nie jest adekwatny do tego jak bardzo ważne były inne cechy)

### Podsumowanie wszystkich testów kwerendy średniozaawansowanej

W ramach kwerendy „Znajdź dzieła które są łatwopalne” analizowaliśmy, czy modele prawidłowo rozpoznają kluczową cechę determinującą możliwość odpowiedzi, czyli pole material. Był to jedyny atrybut dający wystarczającą informację do określenia łatwopalności, dlatego poprawność odpowiedzi była oceniana wyłącznie na podstawie tego, czy `material` otrzymał najwyższy priorytet.

W każdej konfiguracji modeli oraz dla każdego rozmiaru bazy danych (50, 100, 200, 500, 959) wszystkie modele konsekwentnie przypisywały polu `material` priorytet najwyższy (zwykle 90–100). Oznacza to, że:

✔ wszystkie modele poprawnie zrozumiały semantykę zapytania
✔ wszystkie modele prawidłowo identyfikowały które pole jest nośnikiem informacji
✔ niezależnie od liczby rekordów i złożoności inputu, logika priorytetyzacji była stabilna

# Różnice w priorytetach pozostałych cech

Choć `material` zawsze był numerem 1, modele znacząco różniły się w przyznawaniu priorytetów pozostałym polom:

1. Niektóre modele nadawały pozostałym cechom priorytety bliskie zera

np. openai/gpt-oss-20b:groq bardzo często ustawiał wszystkie inne cechy na 0, uznając je za całkowicie nieistotne.

2. Inne modele nadawały szeroki rozkład priorytetów

np. moonshotai/Kimi-K2-Instruct-0905 lub Ling-1T rozkładały priorytety w zakresie od 5 do 90, mimo że większość z tych cech nie miała realnego znaczenia dla odpowiedzi.

3. Modele Cohere i DeepSeek często preferowały umiarkowanie wysokie priorytety dla technique czy type

Choć nie były one potrzebne w tej kwerendzie, te modele traktowały je jako cechy „potencjalnie” pomocne.



# Czy te różnice mają znaczenie?
W kontekście rozumienia kwerendy – NIE:

Dla poprawności odpowiedzi liczyło się jedynie, czy material był najważniejszy, a to spełniały wszystkie modele.

W kontekście późniejszego wykorzystania priorytetów – TAK, może mieć znaczenie:

Jeżeli system filtruje cechy na podstawie progu priorytetów, np.

uwzględnij tylko cechy z priorytetem ≥ 50
to modele takie jak openai/gpt-oss-20b (gdzie wszystkie inne cechy są 0) zachowają się inaczej niż takie jak Ling-1T, które zdarzały się przyznawać priorytety 70–90 polom kompletnie nieistotnym.

Nadmiernie „szeroki” rozkład priorytetów (Ling-1T, Kimi-K2) może sprawiać, że system zacznie niepotrzebnie uwzględniać cechy nieistotne, co wpłynie na:

wydajność wyszukiwania,

liczbę filtrów,

interpretację wyników przez moduły downstream.

Natomiast „minimalistyczny” rozkład (gpt-oss-20b) może z kolei utrudnić przyszłe kwerendy, w których kilka cech jest faktycznie istotnych.

Warto więc odnotować, że choć różnice nie wpływały na sam wynik testowanej kwerendy, to mogłyby wpłynąć na skuteczność systemu w realnych scenariuszach, jeśli kolejne kroki algorytmu opierają się na priorytetach.





# Czy kolejność cech w outputach ma znaczenie?

Wszystkie modele zwracały cechy w różnej kolejności.
Jednak:

✔ kolejność nie powinna być brana pod uwagę przy interpretacji wyników przez system
✔ priorytety są liczbami – a nie pozycją w słowniku
✔ poprawna implementacja downstream powinna sortować po wartości, nie po kolejności

Dlatego choć kolejności w outputach były różne, nie wpływa to na ocenę poprawności ani na logikę łączenia wyników.






# Rozbieżności w zachowaniach modeli – analiza
`openai/gpt-oss-20b`

Bardzo konsekwentny, minimalistyczny rozkład priorytetów

Tylko material dostaje 100, reszta 0–10
→ Model selektywny i bardzo precyzyjny
→ Ale w bardziej złożonych zapytaniach mógłby „pominąć” cechy drugorzędne, lecz istotne

`moonshotai/Kimi-K2` oraz `Ling-1T`

Rozkłady szerokie: 0–100 na wielu cechach

Wysokie priorytety dla cech nieistotnych (np. name, place)
→ Model heurystycznie zakłada, że wiele atrybutów może potencjalnie pomóc
→ Może prowadzić do zbędnego rozszerzania przestrzeni filtracji

`Cohere` (tylko małe bazy)

Zwykle przyznaje wysokie priorytety `material`, `technique`, `type`
→ Widzimy strukturę bardziej uogólniającą, jakby model zakładał, że technika i typ dzieła mogą wpływać na interpretację materiału
→ Dobre intuicyjnie, ale nie zawsze konieczne

`DeepSeek-V3`

- Bardzo stabilny i przewidywalny
- `material` zawsze dominujący
- Pozostałe priorytety raczej niskie, choć nie zerowe
→ Wyważone podejście – model nie ignoruje cech, ale nie faworyzuje niepotrzebnych




# Czy rozkłady priorytetów były adekwatne?
✔ Główny priorytet (material) – zawsze adekwatny
✖ Priorytety dodatkowe – często nieadekwatne w większości modeli

W realnym zapytaniu „łatwopalność” zależy wyłącznie od materiału.
Dlatego wszystkie inne cechy powinny mieć priorytet bliski 0.

Modele:

openai/gpt-oss-20b → najlepsza zgodność z wymaganą semantyką

DeepSeek-V3 → również poprawny, choć mniej radykalny

moonshot/Kimi-K2, Ling-1T, Cohere → zbyt wysoka waga cech drugorzędnych

Rozbieżności te pokazują, że modele różnie interpretują „możliwość potencjalnego wpływu cechy na odpowiedź”, nawet jeśli faktycznie ten wpływ jest zerowy.




# Wnioski końcowe

Wszystkie modele zdały test w kluczowym aspekcie, czyli przypisywaniu najwyższego priorytetu polu material.

Rozkłady pozostałych priorytetów były jednak niespójne, co w przyszłych zastosowaniach mogłoby wpływać na jakość filtracji.

Modele minimalistyczne (gpt-oss-20b) są teoretycznie najbardziej semantycznie poprawne dla takich kwerend.

Modele heurystyczne (Kimi-K2, Ling-1T) mogą generować nadmiarowe filtry, co zwiększa koszt przeszukiwania.

Kolejność cech w outputach nie ma znaczenia i nie powinna być wykorzystywana przez system downstream.

Najważniejsza obserwacja: niezależnie od liczby rekordów (50 → 959), żaden model nie zgubił priorytetu material, co świadczy o stabilnym rozumieniu zadania.

W związku z tym, uważamy że w wypadku kwerendy typu średniozaawansowanego, modele mogą być używane w aplikacjach, ale trzeba wziąć pod uwagę zarówno zachowanie konkretnego modelu jak i to w jaki sposób przefiltrujemy priorytety które są nam potrzebne.













# -------------------------------
# | TEST 3 - KWERENDA TRYWIALNA |
# -------------------------------

Test trzeci - trywialna kwerenda
"query": "Znajdź dzieła przedstawiające ludzi"

# Dlaczego ta kwerenda jest trywialna?

1. Wymaga wzięcia pod uwagę tylko pola `name`

2. Nie wymaga brania pod uwagę wartości cech obiektu, same cechy wystarczyłyby do odpowiedzi na tę kwerendę

3. Inne pola praktycznie nie mają wpływu na odpowiedź



W tej części badań badamy tylko:
- czy pole `name` uzyskało najwyższy priorytet


jeżeli tak, określamy że model odpowiedział poprawnie.







### Pierwszy test na bazie danych o ilości obiektów 50:

{'output': {'name': 90, 'type': 70, 'technique': 50, 'material': 40, 'size': 30, 'place': 20, 'createdate': 10, 'copyright': 5, 'creator': 5, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 4.278}
{'output': {'name': 100, 'creator': 0, 'inventorynumber': 0, 'createdate': 0, 'size': 0, 'material': 0, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.116}
{'output': {'inventorynumber': 5, 'createdate': 5, 'name': 100, 'size': 5, 'material': 10, 'technique': 10, 'place': 20, 'type': 30, 'copyright': 5, 'creator': 20}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.948}
{'output': {'name': 100, 'creator': 70, 'type': 60, 'place': 50, 'technique': 40, 'material': 30, 'size': 20, 'createdate': 10, 'inventorynumber': 0, 'copyright': 0}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.76}
{'output': {'name': 95, 'creator': 85, 'place': 80, 'type': 75, 'technique': 70, 'material': 65, 'size': 50, 'createdate': 60, 'inventorynumber': 40, 'copyright': 30}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 8.607}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
CohereLabs/command-a-translate-08-2025:cohere - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE



## Drugi test na bazie danych o ilości obiektów 50:

{'output': {'name': 90, 'type': 70, 'creator': 60, 'place': 50, 'createdate': 40, 'material': 30, 'technique': 20, 'size': 10, 'inventorynumber': 0, 'copyright': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 3.795}
{'output': {'name': 100, 'creator': 0, 'inventorynumber': 0, 'createdate': 0, 'size': 0, 'material': 0, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.22}
{'output': {'inventorynumber': 5, 'createdate': 5, 'name': 100, 'size': 10, 'material': 10, 'technique': 10, 'place': 20, 'type': 20, 'copyright': 5, 'creator': 15}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.739}
{'output': {'name': 100, 'creator': 80, 'type': 60, 'place': 40, 'technique': 20, 'material': 10, 'size': 5, 'createdate': 1, 'inventorynumber': 0, 'copyright': 0}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 3.276}
{'output': {'name': 100, 'type': 90, 'creator': 80, 'place': 80, 'createdate': 70}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 5.729}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
CohereLabs/command-a-translate-08-2025:cohere - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

# Trzeci test na bazie danych o ilości obiektów 50:

{'output': {'name': 90, 'type': 70, 'technique': 60, 'material': 50, 'size': 40, 'place': 30, 'createdate': 20, 'creator': 10, 'copyright': 5, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 4.111}
{'output': {'name': 100, 'creator': 0, 'inventorynumber': 0, 'createdate': 0, 'size': 0, 'material': 0, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.348}
{'output': {'inventorynumber': 10, 'createdate': 20, 'name': 90, 'size': 15, 'material': 10, 'technique': 10, 'place': 10, 'type': 60, 'copyright': 10, 'creator': 25}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.552}
{'output': {'name': 100, 'creator': 70, 'type': 60, 'place': 50, 'technique': 40, 'material': 30, 'size': 20, 'createdate': 10, 'inventorynumber': 0, 'copyright': 0}, 'model': 'CohereLabs/command-a-translate-08-2025:cohere', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.362}
{'output': {'name': 100, 'creator': 85, 'place': 70, 'createdate': 65, 'type': 60, 'technique': 55, 'material': 40, 'size': 30, 'inventorynumber': 20, 'copyright': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 7.833}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
CohereLabs/command-a-translate-08-2025:cohere - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE


# Podsumowanie testu na bazie danych o ilości obiektów 50:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `name` uzyskało najwyższy priorytet


!!!
Pominięto testy na modelu CohereLabs/command-a-translate-08-2025:cohere na większych bazach danych
ze względu na problemy z limitem kontekstu wspomiane na początku raportu.
!!!

### Pierwszy test na bazie danych o ilości obiektów 100:

{'output': {'name': 100, 'type': 80, 'technique': 60, 'material': 40, 'size': 30, 'place': 20, 'createdate': 10, 'copyright': 5, 'creator': 5, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 3.729}
{'output': {'name': 100, 'inventorynumber': 0, 'createdate': 0, 'size': 0, 'material': 0, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0, 'creator': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.735}
{'output': {'inventorynumber': 10, 'createdate': 20, 'name': 90, 'size': 10, 'material': 5, 'technique': 5, 'place': 30, 'type': 80, 'copyright': 5, 'creator': 50}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.157}
{'output': {'name': 100, 'type': 80, 'technique': 60, 'place': 70, 'creator': 50, 'createdate': 90, 'size': 20, 'material': 30, 'inventorynumber': 10, 'copyright': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 7.772}


deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

## Drugi test na bazie danych o ilości obiektów 100:

{'output': {'name': 100, 'type': 80, 'technique': 60, 'material': 40, 'place': 20, 'creator': 10, 'createdate': 5, 'size': 0, 'inventorynumber': 0, 'copyright': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 5.778}
{'output': {'name': 100, 'creator': 0, 'type': 0, 'place': 0, 'createdate': 0, 'material': 0, 'technique': 0, 'size': 0, 'copyright': 0, 'inventorynumber': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.534}
{'output': {'inventorynumber': 0, 'createdate': 0, 'name': 100, 'size': 0, 'material': 0, 'technique': 0, 'place': 0, 'type': 90, 'copyright': 0, 'creator': 70}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.938}
{'output': {'name': 100, 'creator': 90, 'place': 85, 'createdate': 80, 'type': 70, 'technique': 70, 'material': 60, 'size': 50, 'inventorynumber': 40, 'copyright': 30}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 9.314}


deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

# Trzeci test na bazie danych o ilości obiektów 100:

{'output': {'name': 100, 'type': 80, 'technique': 60, 'material': 40, 'place': 20, 'creator': 10, 'copyright': 5, 'size': 5, 'createdate': 5, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 3.965}
{'output': {'name': 100, 'type': 80, 'creator': 60, 'createdate': 40, 'place': 30, 'technique': 20, 'material': 10, 'size': 5, 'copyright': 5, 'inventorynumber': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 0.709}
{'output': {'name': 100, 'type': 80, 'creator': 60, 'createdate': 50, 'inventorynumber': 40, 'place': 30, 'size': 30, 'material': 20, 'technique': 20, 'copyright': 10}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.462}
{'output': {'name': 95, 'creator': 85, 'place': 80, 'createdate': 75, 'type': 70, 'technique': 60, 'material': 55, 'size': 40, 'inventorynumber': 30, 'copyright': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 7.572}


deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE

# Podsumowanie testu na bazie danych o ilości obiektów 100:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `name` uzyskało najwyższy priorytet


### Pierwszy test na bazie danych o ilości obiektów 200:

{'output': {'name': 90, 'type': 80, 'technique': 70, 'material': 60, 'size': 50, 'place': 40, 'createdate': 30, 'creator': 20, 'copyright': 10, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 6.031}
{'output': {'name': 100, 'creator': 0, 'inventorynumber': 0, 'createdate': 0, 'size': 0, 'material': 0, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.861}
{'output': {'inventorynumber': 30, 'createdate': 20, 'name': 100, 'size': 10, 'material': 5, 'technique': 5, 'place': 5, 'type': 80, 'copyright': 5, 'creator': 50}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.354}
{'output': {'name': 100, 'creator': 80, 'place': 70, 'createdate': 60, 'technique': 50, 'material': 40, 'size': 30, 'inventorynumber': 20, 'copyright': 10, 'type': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 10.022}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE


## Drugi test na bazie danych o ilości obiektów 200:

{'output': {'name': 90, 'type': 80, 'creator': 70, 'place': 60, 'createdate': 50, 'material': 40, 'technique': 30, 'size': 20, 'inventorynumber': 10, 'copyright': 5}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 5.054}
{'output': {'name': 100, 'creator': 0, 'inventorynumber': 0, 'createdate': 0, 'size': 0, 'material': 0, 'technique': 0, 'place': 0, 'type': 0, 'copyright': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.025}
{'output': {'name': 95, 'type': 95, 'creator': 75, 'place': 40, 'size': 20, 'material': 20, 'technique': 20, 'copyright': 10, 'createdate': 10, 'inventorynumber': 5}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.769}
{'output': {'name': 100, 'creator': 90, 'place': 80, 'createdate': 70, 'technique': 60, 'material': 50, 'size': 40, 'type': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 10.02}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - NIEPOPRAWNE - zarówno `name` jak i `type` miały ten sam priorytet.
inclusionAI/Ling-1T:featherless-ai - POPRAWNE


# Trzeci test na bazie danych o ilości obiektów 200:

{'output': {'name': 90, 'type': 70, 'creator': 60, 'place': 50, 'createdate': 40, 'material': 30, 'technique': 20, 'size': 10, 'copyright': 5, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 5.126}
{'output': {'name': 100, 'type': 80, 'creator': 60, 'createdate': 40, 'place': 30, 'technique': 20, 'material': 10, 'size': 5, 'copyright': 5, 'inventorynumber': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.65}
{'output': {'inventorynumber': 10, 'createdate': 20, 'name': 90, 'size': 10, 'material': 10, 'technique': 10, 'place': 20, 'type': 60, 'copyright': 5, 'creator': 70}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.862}
{'output': {'name': 100, 'type': 80, 'creator': 70, 'technique': 60, 'place': 50, 'material': 40, 'size': 30, 'createdate': 20, 'inventorynumber': 10, 'copyright': 5}, 'model': 'inclusionAI/Ling-1T:featherless-ai', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 7.164}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE
inclusionAI/Ling-1T:featherless-ai - POPRAWNE


# Podsumowanie testu na bazie danych o ilości obiektów 200:

Oprócz modelu `openai/gpt-oss-20b:groq`
wszystkie inne poprawnie odpowiedziały na kwerendę.

Model `openai/gpt-oss-20b:groq` popełnił błąd przy drugim wykonaniu, nadając `name` i `type` ten sam priorytet 95. Taka odpowiedź mogłaby spowodować błędne działanie systemu.



### Pierwszy test na bazie danych o ilości obiektów 500:

{'output': {'name': 90, 'type': 80, 'technique': 70, 'material': 60, 'size': 50, 'place': 40, 'creator': 30, 'createdate': 20, 'copyright': 10, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 9.458}
{'output': {'name': 100, 'creator': 90, 'type': 80, 'createdate': 70, 'place': 60, 'material': 50, 'technique': 40, 'size': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 5.325}
{'output': {'inventorynumber': 0, 'createdate': 10, 'name': 90, 'size': 20, 'material': 5, 'technique': 5, 'place': 15, 'type': 40, 'copyright': 5, 'creator': 70}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 4.895}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE


## Drugi test na bazie danych o ilości obiektów 500:

{'output': {'name': 90, 'type': 80, 'creator': 70, 'createdate': 60, 'place': 50, 'technique': 40, 'material': 30, 'size': 20, 'copyright': 10, 'inventorynumber': 0}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 9.855}
{'output': {'name': 100, 'type': 0, 'creator': 0, 'createdate': 0, 'material': 0, 'technique': 0, 'place': 0, 'size': 0, 'copyright': 0, 'inventorynumber': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 5.308}
{'output': {'inventorynumber': 5, 'createdate': 5, 'name': 100, 'size': 10, 'material': 20, 'technique': 20, 'place': 30, 'type': 70, 'copyright': 5, 'creator': 50}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 4.819}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE

# Trzeci test na bazie danych o ilości obiektów 500:

{'output': {'name': 100, 'type': 90, 'creator': 80, 'createdate': 70, 'place': 60, 'material': 50, 'technique': 40, 'size': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 9.743}
{'output': {'name': 100, 'creator': 80, 'type': 60, 'place': 40, 'createdate': 30, 'material': 20, 'technique': 20, 'size': 10, 'copyright': 5, 'inventorynumber': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 5.205}
{'output': {'name': 100, 'creator': 80, 'type': 50, 'place': 30, 'material': 20, 'technique': 20, 'createdate': 10, 'inventorynumber': 5}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.704}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE


# Podsumowanie testu na bazie danych o ilości obiektów 500:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `name` uzyskało najwyższy priorytet



### Pierwszy test na bazie danych o ilości obiektów 959:

{'output': {'name': 100, 'type': 90, 'creator': 80, 'place': 70, 'createdate': 60, 'material': 50, 'technique': 40, 'size': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 38.841}
{'output': {'name': 100, 'type': 90, 'creator': 80, 'createdate': 70, 'place': 60, 'technique': 50, 'material': 40, 'size': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 9.237}
{'output': {'inventorynumber': 0, 'createdate': 5, 'name': 100, 'size': 10, 'material': 20, 'technique': 20, 'place': 10, 'type': 80, 'copyright': 0, 'creator': 10}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 7.771}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE

## Drugi test na bazie danych o ilości obiektów 959:

{'output': {'name': 100, 'type': 90, 'creator': 80, 'createdate': 70, 'place': 60, 'material': 50, 'technique': 40, 'size': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 38.127}
{'output': {'name': 100, 'creator': 75, 'copyright': 50, 'type': 25, 'material': 0, 'technique': 0, 'size': 0, 'createdate': 0, 'place': 0, 'inventorynumber': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 9.184}
{'output': {'inventorynumber': 0, 'createdate': 40, 'name': 100, 'size': 30, 'material': 20, 'technique': 20, 'place': 40, 'type': 80, 'copyright': 10, 'creator': 60}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 7.344}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE


# Trzeci test na bazie danych o ilości obiektów 959:

{'output': {'name': 100, 'type': 90, 'creator': 80, 'place': 70, 'createdate': 60, 'material': 50, 'technique': 40, 'size': 30, 'copyright': 20, 'inventorynumber': 10}, 'model': 'deepseek-ai/DeepSeek-V3-0324', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 42.527}
{'output': {'name': 100, 'creator': 80, 'createdate': 30, 'place': 20, 'type': 10, 'material': 5, 'technique': 5, 'size': 5, 'copyright': 0}, 'model': 'moonshotai/Kimi-K2-Instruct-0905', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 1.308}
{'output': {'inventorynumber': 0, 'createdate': 10, 'name': 100, 'size': 0, 'material': 0, 'technique': 30, 'place': 10, 'type': 80, 'copyright': 0, 'creator': 20}, 'model': 'openai/gpt-oss-20b:groq', 'query': 'Znajdź dzieła przedstawiające ludzi', 'elapsed_time': 2.691}

deepseek-ai/DeepSeek-V3-0324 - POPRAWNE
moonshotai/Kimi-K2-Instruct-0905 - POPRAWNE
openai/gpt-oss-20b:groq - POPRAWNE


# Podsumowanie testu na bazie danych o ilości obiektów 959:

Wszystkie modele poprawnie odpowiedziały na problem:
- czy pole `name` uzyskało najwyższy priorytet








### Podsumowanie wszystkich testów kwerendy trywialnej:

Podsumowanie wszystkich testów kwerendy trywialnej

Kwerenda „Znajdź dzieła przedstawiające ludzi” była najprostszą ze wszystkich trzech testowanych zapytań i wymagała uwzględnienia wyłącznie jednej cechy: name. Wystarczy bowiem, aby nazwa obiektu zawierała informację o przedstawieniu ludzi, więc żadna inna cecha nie powinna mieć wpływu na wynik priorytetyzacji.
Celem testu było ustalenie, czy modele poprawnie przypiszą najwyższy priorytet polu name, niezależnie od wielkości bazy danych.

1. Ogólne wyniki

W zdecydowanej większości przypadków wszystkie modele przypisały polu name najwyższą wartość priorytetu, spełniając tym samym podstawowy warunek poprawności.
Dotyczy to wszystkich rozmiarów baz danych (50, 100, 200, 500, 959 obiektów) oraz wielu powtórzeń testów.

Wyniki ogólne:

DeepSeek-V3 — 100% poprawnych wyników

Kimi-K2 — 100% poprawnych wyników

Cohere (tam gdzie użyty) — 100% poprawnych wyników

Ling-1T — 100% poprawnych wyników

gpt-oss-20b (Groq) — 1 błąd na 15 testów

Tym samym jedyny błąd w całym teście trywialnym pochodził od modelu openai/gpt-oss-20b:groq.

2. Pojedynczy błąd modelu gpt-oss-20b:groq — analiza ryzyka

W jednym z testów na bazie o rozmiarze 200 obiektów model gpt-oss-20b przypisał:

name: 95

type: 95

czyli cecha kluczowa i cecha niekluczowa otrzymały identyczny priorytet.

Taki wynik jest formalnie niepoprawny, ponieważ wprowadza niejednoznaczność do systemu filtracji, który oczekuje wskazania cechy dominującej.
Skutki potencjalne:

błędna filtracja danych,

niepoprawne wyniki wyszukiwania,

niestabilność systemu przy zautomatyzowanych procesach,

ryzyko propagowania błędu w kolejnych krokach algorytmu.

Choć statystycznie jest to 1 błąd na 15 testów (≈ 6,7%), należy podkreślić, że:

test był najprostszy ze wszystkich,

oczekiwana poprawność powinna wynosić 100%,

błąd w kwerendzie trywialnej sugeruje potencjalne problemy przy bardziej złożonych zapytaniach,

minimalna liczba testów nie pozwala oszacować rzeczywistego ryzyka — realna częstotliwość błędów może być większa lub mniejsza.

Błąd ten zdecydowanie osłabia zaufanie do modelu w zastosowaniach produkcyjnych wymagających deterministycznej klasyfikacji cech.

3. Rozkład priorytetów w innych modelach — nieadekwatność drugorzędnych cech

Choć pozostałe modele nie popełniły błędów formalnych (pole name zawsze było na pierwszym miejscu), wiele z nich wykazywało zaskakującą tendencję do nadawania bardzo wysokich priorytetów cechom nieistotnym, w szczególności:

type (często 70–95!),

creator,

place,

createdate,

technique.

W kontekście kwerendy trywialnej takie zachowania są semantycznie nieuzasadnione, ponieważ żadna z tych cech nie wnosi informacji o tym, czy dzieło przedstawia ludzi.

Skutki tego zjawiska:

Ryzyko nadmiernej filtracji — system mógłby zastosować niepotrzebne filtry.

Obciążenie algorytmów downstream — większa liczba cech traktowanych jako istotne.

Zwiększona złożoność i gorsza interpretowalność wyniku — użytkownik lub kolejny moduł może uznać wysokie priorytety za sygnał istotności.

Potencjalne błędy w innych, bardziej złożonych kwerendach — jeśli modele nie potrafią odpowiednio „wyłączyć” nieistotnych cech w najprostszym przypadku, mogą nadmiernie komplikować analizę w przypadkach trudniejszych.

Najbardziej „zdyscyplinowany” pod względem semantyki był:

openai/gpt-oss-20b (Groq) — co paradoksalnie czyni jego jedyny błąd jeszcze bardziej zaskakującym,

Kimi-K2 — regularnie przypisujący bardzo niskie lub zerowe priorytety cechom niepotrzebnym.

Z kolei Ling-1T i częściowo Cohere często generowały rozbudowane, szeroko rozciągnięte rozkłady priorytetów, które, choć formalnie poprawne, nie odpowiadały logice zadania.

4. Zaskoczenie wynikiem – dlaczego to ważne?

Oczekiwaliśmy, że kwerenda trywialna przejdzie bezbłędnie w 100% przypadków, ponieważ:

jest prostsza niż pozostałe dwie kwerendy,

wymaga uwzględnienia tylko jednej cechy (name),

nie wymaga żadnej interpretacji zależności między cechami,

nie wymaga analizowania wartości cech.

Fakt, że błąd wystąpił właśnie tutaj, a nie w kwerendach trudniejszych, jest nieintuicyjny.
Sugeruje to, że:

modele mogą od czasu do czasu działać niedeterministycznie,

drobne różnice w kontekście lub wewnętrznych heurystykach mogą powodować nieprzewidywalne odchylenia,

stosowanie ich w systemach, gdzie poprawność=konieczność, może być ryzykowne.

W praktyce oznacza to, że choć rozwiązanie jest nowatorskie i potencjalnie użyteczne, automatyczny system oparty wyłącznie na priorytetyzacji cech przez modele językowe nie może być w 100% samodzielny. Nadal wymagałby:

nadzoru ludzkiego,

dodatkowych warstw weryfikacji,

mechanizmów wykrywania priorytetów równych,

fallbacków w przypadku niepewności,

lub algorytmicznej korekty wyników modelu.

5. Wnioski końcowe

Modele niemal zawsze ustalały właściwy priorytet (name)
— z wyjątkiem jednego błędu gpt-oss-20b.

Jedyny błąd w najprostszym teście jest istotny
— bo pokazuje, że nawet banalne kwerendy mogą być zagrożone losową niepoprawnością.

Rozkłady priorytetów były często nieadekwatne semantycznie
— wiele modeli nadawało wysokie priorytety cechom, które nie mają związku z zadaniem.

System wykorzystujący takie priorytety wymaga mechanizmów zabezpieczających
— aby uniknąć niejednoznaczności i niepoprawnej filtracji.

Nowatorskość rozwiązania jest widoczna, ale nie zapewnia standardu bezbłędności
— wymaganego w nowoczesnych systemach wyszukiwawczych.

Dalsze testy byłyby wskazane, aby lepiej oszacować rzeczywistą częstotliwość tego typu błędów i ich zależność od kontekstu, rozmiaru danych i wewnętrznej zmienności modeli.






# ##################
# # CZAS WYKONANIA #
# ##################


Czas wykonania mierzyliśmy korzystając z biblioteki `timeit`
# //TODO: zawrzeć informacje o pingu i że był niski (~13ms), więc pominęliśmy jego wpływ na czas wykonania samego modelu, jak również pominęliśmy różnice w czasie odpowiedzi od różnych dostawców (korzystamy na ten moment tylko z api zapewnionego przez huggingface, także opóźnienia u huggingface = opóźnienia wykonania w naszych testach - nie były mierzone ani brane pod uwagę)

Część kodu odpowiadająca za pomiar czasu:


> Plik `src/ai_search.py`

```
start = timer()
msg = self.get_response(query, db, model)
end = timer()
elapsed_time = round(end - start, 3)  # rounds to 3 decimal places (0.001 precision)
```

Funkcja get_response():

> Plik `src/ai_search.py`
```
def get_response(self, query, db, model):
        response = self.api_handler.send_request(query, db, "huggingface", model)
        msg = response.choices[0].message.content
        logging.getLogger(__name__).info(msg)

        return msg
```

Korzystająca z metody klasy ApiHandler, zawartego w pliku:
`src/api_handler.py`



# //TODO: zrobić tabelki i statystyki dla czasów wykonań, porównania etc. weź pod uwagę przy robieniu statystyk że nie wszystkie modele dotarły do końcowej wielkości bazy danych ze względu na limity kontekstu (wytłumaczone na początku raportu)







# ########
# KOSZTA #
# ########

Koszta i realność użycia takiego rozwiązania:

Do obliczenia ilości tokenów dla poszczególnych edycji baz danych wykorzystaliśmy narzędzie:
https://token-calculator.net/

Dane pobraliśmy z internetu, promptów Gemini i stron danych modelów:
https://docs.together.ai/docs/kimi-k2-quickstart
https://zenmux.ai/inclusionai/ling-1t
https://blog.galaxy.ai/compare/llama-3-1-8b-instruct-vs-llama-3-8b-instruct
https://huggingface.co/CohereLabs/command-a-translate-08-2025
https://developers.cloudflare.com/workers-ai/models/gpt-oss-20b/
https://pricepertoken.com/pricing-page/model/deepseek-deepseek-chat-v3-0324


Pominęliśmy koszt output tokenów ze względu na ich znikomą ilość w porównaniu do inputu (cała baza danych + kwerenda)
Nie wzięliśmy też pod uwagę ile tokenów zabiera kwerenda i asysta promptu (`self.ai_prompt_assist`) z powodów j.w.


Wyjaśnienie terminów:
Token - najmniejsza jednostka tekstu jaką model AI może przetworzyć, taka jak słowo, część słowa, lub znak interpunkcyjny
Context - kontekst modelu, czyli ilość tokenów które może przyjąć w jednym zapytaniu
Input tokens - jednostki tekstu które przesyłamy do modelu (mają własny koszt)
Output tokens - jednostki tekstu które model zwraca (mają własny koszt)

Poniżej zamieszczamy tabelę kosztów dla użytych do badań modelów:


Model	                                Context	        $ per 1M input tokens
DeepSeek-V3-0324	                160k	        $0.24
Kimi-K2-Instruct-0905                   ~262k           $1.00
gpt-oss-20b                             ~128k           $0.03 - $0.20, avg: 0.12$
CohereLabs/command-a-translate-08-2025  16k             Free
inclusionAI/Ling-1T                     128K            $0.56
meta-llama/Llama-3.1-8B-Instruct        128k            $0.02

Koszta różnią się w zależności kto zapewnia nam dostęp do modelu (pośrednicy)







Poglądowo:
# //TODO: tabelki do podsumowania tej części raportu bo nikt sie w tym nie rozczyta, obliczenia nie są ważne tylko końcowe wartości

# Koszta dla danych o ilości obiektów 50:
Ilość tokenów: 6782
DeepSeek-V3-0324: $0.0016 (0.006782 * $0.24)
Kimi-K2-Instruct-0905: $0.0068 (0.006782 * $1.00)
gpt-oss-20b: $0.0008 (0.006782 * $0.12)
CohereLabs/command-a-translate: $0 (Free)
inclusionAI/Ling-1T: $0.0038 (0.006782 * $0.56)
meta-llama/Llama-3.1-8B-Instruct: $0.0001 (0.006782 * $0.02)

# Koszta dla danych o ilości obiektów 100:
Ilość tokenów: 13473
DeepSeek-V3-0324: $0.0032 (0.013473 * $0.24)
Kimi-K2-Instruct-0905: $0.0135 (0.013473 * $1.00)
gpt-oss-20b: $0.0016 (0.013473 * $0.12)
CohereLabs/command-a-translate: $0 (Free)
inclusionAI/Ling-1T: $0.0075 (0.013473 * $0.56)
meta-llama/Llama-3.1-8B-Instruct: $0.0003 (0.013473 * $0.02)

# Koszta dla danych o ilości obiektów 200:
Ilość tokenów: 27009
DeepSeek-V3-0324: $0.0065 (0.027009 * $0.24)
Kimi-K2-Instruct-0905: $0.0270 (0.027009 * $1.00)
gpt-oss-20b: $0.0032 (0.027009 * $0.12)
CohereLabs/command-a-translate: $0 (Free)
inclusionAI/Ling-1T: $0.0151 (0.027009 * $0.56)
meta-llama/Llama-3.1-8B-Instruct: $0.0005 (0.027009 * $0.02)

# Koszta dla danych o ilości obiektów 500:
Ilość tokenów: 67300
DeepSeek-V3-0324: $0.0161 (0.067300 * $0.24)
Kimi-K2-Instruct-0905: $0.0673 (0.067300 * $1.00)
gpt-oss-20b: $0.0081 (0.067300 * $0.12)
CohereLabs/command-a-translate: $0 (Free)
inclusionAI/Ling-1T: $0.0377 (0.067300 * $0.56)
meta-llama/Llama-3.1-8B-Instruct: $0.0013 (0.067300 * $0.02)

# Koszta dla danych o ilości obiektów 959:
Ilość tokenów: 129206
DeepSeek-V3-0324: $0.0310 (0.129206 * $0.24)
Kimi-K2-Instruct-0905: $0.1292 (0.129206 * $1.00)
gpt-oss-20b: $0.0155 (0.129206 * $0.12)
CohereLabs/command-a-translate: $0 (Free, ale przekracza context 16k)
inclusionAI/Ling-1T: $0.0724 (0.129206 * $0.56)
meta-llama/Llama-3.1-8B-Instruct: $0.0026 (0.129206 * $0.02)

# Przykłady kosztów dla innych typów baz danych:


# //TODO: wejść na te linki i sprawdzić czy dane zgadzają się z tym co jest na tych stronach

## 1. Kaggle - Netflix Movies and TV Shows
Link: https://www.kaggle.com/datasets/shivamb/netflix-shows
Rozmiar: ~8700 wpisów, ~12 kolumn
Szacowana ilość tokenów: ~950,000 tokenów (pełna baza)

Koszta na zapytanie (pełna baza):
- DeepSeek-V3-0324: $0.23
- Kimi-K2-Instruct-0905: $0.95
- gpt-oss-20b: $0.11
- inclusionAI/Ling-1T: $0.53
- meta-llama/Llama-3.1-8B-Instruct: $0.019

## 2. UCI Machine Learning Repository - Wine Quality Dataset
Link: https://archive.ics.uci.edu/dataset/186/wine+quality
Rozmiar: ~6500 wpisów, 12 kolumn (wartości numeryczne)
Szacowana ilość tokenów: ~85,000 tokenów

Koszta na zapytanie:
- DeepSeek-V3-0324: $0.020
- Kimi-K2-Instruct-0905: $0.085
- gpt-oss-20b: $0.010
- inclusionAI/Ling-1T: $0.048
- meta-llama/Llama-3.1-8B-Instruct: $0.0017

## 3. Data.gov - US Baby Names
Link: https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-data
Rozmiar: ~2 miliony wpisów, 5 kolumn
Szacowana ilość tokenów: ~18,000,000 tokenów
Uwaga: Wymaga chunking/partycjonowania

Koszt dla fragmentu 100k tokenów:
- DeepSeek-V3-0324: $0.024
- Kimi-K2-Instruct-0905: $0.10
- gpt-oss-20b: $0.012
- inclusionAI/Ling-1T: $0.056
- meta-llama/Llama-3.1-8B-Instruct: $0.002

## 4. World Bank Open Data - World Development Indicators
Link: https://datacatalog.worldbank.org/search/dataset/0037712
Rozmiar: ~1500 wskaźników, ~200 krajów, dane roczne
Szacowana ilość tokenów: ~450,000 tokenów (ostatnie 10 lat)

Koszta na zapytanie:
- DeepSeek-V3-0324: $0.11
- Kimi-K2-Instruct-0905: $0.45
- gpt-oss-20b: $0.054
- inclusionAI/Ling-1T: $0.25
- meta-llama/Llama-3.1-8B-Instruct: $0.009

## 5. GitHub - Awesome Public Datasets - NYC Taxi Data
Link: https://github.com/awesomedata/awesome-public-datasets
Rozmiar: ~1.5 miliona przejazdów/miesiąc, ~20 kolumn
Szacowana ilość tokenów: ~2,500,000 tokenów (miesiąc danych)
Uwaga: Wymaga chunking

Koszt dla fragmentu 128k tokenów (limit większości modeli):
- DeepSeek-V3-0324: $0.031
- Kimi-K2-Instruct-0905: $0.128
- gpt-oss-20b: $0.015
- inclusionAI/Ling-1T: $0.072
- meta-llama/Llama-3.1-8B-Instruct: $0.0026

## 6. OpenML - Titanic Dataset
Link: https://www.openml.org/search?type=data&status=active&id=40945
Rozmiar: 891 wpisów, 12 kolumn
Szacowana ilość tokenów: ~11,500 tokenów

Koszta na zapytanie:
- DeepSeek-V3-0324: $0.0028
- Kimi-K2-Instruct-0905: $0.0115
- gpt-oss-20b: $0.0014
- inclusionAI/Ling-1T: $0.0064
- meta-llama/Llama-3.1-8B-Instruct: $0.00023

Wnioski:
- Dla małych baz (< 1000 wpisów): Koszta minimalne ($0.001 - $0.13 per query)
- Dla średnich baz (1000-10000 wpisów): Koszta umiarkowane ($0.02 - $1.00 per query)
- Dla dużych baz (> 10000 wpisów): Wymagany chunking, koszta mogą być znaczące
- Najtańszy: Llama-3.1-8B ($0.02/1M tokens), ale nie można na nim polegać
- Najbardziej ekonomiczny kompromis: DeepSeek-V3 ($0.24/1M tokens) z największym context (160k)













# #########
# WNIOSKI #
# #########




Wnioski:
Na modelach nie można było polegać w taki sposób że ustalenie progu do jakiego cechy mają znaczenie jest problematyczne i jedyne rozwiązanie jakie wymyśliliśmy, to zawrzeć w promptcie kolejny warunek że priorytety mają przestrzegać danego progu (np. większy bądź równy 50).
Jednakże taki warunek nie jest optymalny dla każdej kwerendy - przy niektórych kwerendach oczekujemy naturalnego rozstawienia priorytetów, próg nie jest stały, a z takim promptem modele mogły by rozkładać priorytety "na siłę" poniżej lub powyżej danego progu, a priorytet danej cechy nie odpowiadał by jej realnemu znaczeniu w kontekście kwerendy.
# //TODO: jakieś źródło o overfittingu/underfittingu LLMów przy złej kwerendzie (opcjonalne)

Jest sens testować na bazie danych o małej jak i dużej ilości cech, zarówno relatywnej jak i nosql, bo zapewnia to użytkownikowi szybsze przefiltrowanie cech które mają największe znaczenie.
Jednak nie można polegać na modelach AI by automatycznie określały które konkretnie cechy powinny zostać do filtracji - użytkownik sam musi określić jaki próg lub zakres priorytetów akceptuje
Sens takiego rozwiązania jest wtedy gdy użytkownik potrzebuje listy priorytetów do ułatwienia dalszej filtracji, ale nie zastąpi finalnie ręcznej (lub programistycznej) filtracji ze względu na brak dokładności i subiektywność modelów.
Na pewno jest to rozwiązanie które może wspierać filtracje danych, szybko pokazuje które cechy są najważniejsze i nadaje niskie priorytety tym które nie są ważne, ale nie zastąpi ręcznej filtracji.
Sytuacja w której można by zastąpić ręczną filtrację całkowicie zachodzi tylko z pomocą programistów którzy już wykonali dane kwerendy i wiedzą jakiej odpowiedzi sie spodziewać - twierdzimy na podstawie testów z poprzednich raportów, że modele są w większości konsekwentne w swoich odpowiedziach co do priorytetów (pomijając modele które zostały usunięte z dalszych testów ze względu na brak konsekwentności). Wtedy można polegać na ustalaniu progów dla każdej konkretnej kwerendy i bazy danych.


# //TODO: Wnioski dlaczego taki system nadaje się naszym zdaniem tylko do wspomagania procesu filtracji, ale nie będzie w stanie jej zastąpić bo nie zapewnia zawsze idealnych wyników, a subiektywność modeli odbiega od realnego rozłożenia priorytetów (szczególnie widoczne na Teście 3 - kwerenda trywialna). Zastanawiające jest to, że przy trudniejszych kwerendach modele radziły sobie lepiej.

# //TODO: Wnioski o tym że modyfikacja kwerendy dodatkowej być może mogła by zapewnić lepsze rezultaty i wymagane są dodatkowe badania w tym kierunku (optymalizacja rozwiązań)

# //TODO: Wnioski o limicie kontekstu, rozwiązanie - wysyłanie kilku zapytań z podzieloną bazą danych w zakresie kontekstu modelu
# //TODO: proponowane kolejne rozwiązanie (optymalizacja) na masywne ilości tokenów - wysłanie tylko unikalnych cech i unikalnych wartości odpowiadających tym cechom w bazie danych. problemy z tym rozwiązaniem - nie jest adekwatne dla każdej bazy danych, może powodować problemy z ustaleniem odpowiednich priorytetów (wymaga dalszych badań). Bazy danych które nie mają wielu unikatowych wartości mogą z tego skorzystać i wyjść bardzo efektywnie pod względem kosztów, ale bazy które mają wiele różnych wartości - nie będzie to ogromna optymalizacja.

# //TODO: kolejne proponowane rozwiązanie - fine-tuning jakiegoś modelu do naszej konkretnej bazy danych, potencjalnie rozwiązanie tańsze i celniejsze, ale wymaga dodatkowych badań czy ma sens, dodatkowo jest względnie trudniejsze do wykonania, zazwyczaj wymaga dłuższego czasu trenowania i testów, uważamy że takie rozwiązanie zazwyczaj nie będzie lepsze od standardowego filtrowania bazy danych "ręcznie"

# //TOOD: Wnioski o ilości czasu, czy to długie wykonanie, czy warto z tego korzystać, przewidywania jak się to będzie prezentowało na większych bazach danych (powyżej 200 000 tokenów), może jakiś wykres do przewidywania tego czasu wykonania
# //TODO: Wady i zalety naszego rozwiązania







