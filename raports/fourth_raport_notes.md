
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
# //TODO: tu dopisać lepszy, bardziej szczegółowy opis bazy danych


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




Wykonaliśmy testy modelów na trzech kwerendach o różnej trudności ustalenia priorytetów cech.
# //TODO: rozpisać trzy kwerendy na których były prowadzone badania i ich zróżnicowanie w trudności odpowiedzi
Kwerenda zaawansowana: 
> "Znajdź dzieła wykonane w trakcie wojny w danym państwie"
Kwerenda średniozaawansowana: 
> XXX
Kwerenda trywialna: 
> YYY

Kwerenda dodatkowa pozostała bez zmian od poprzednich testów:
self.ai_prompt_assist = "### Dla podanej wcześniej kwerendy ustal priorytety pól (object properties) danych które najbardziej jej odpowiadają i zwróć tylko jeden obiekt wszystkich pól razem z ich priorytetami - wyższy priorytet znaczy lepsze dopasowanie, jedyny tekst jaki masz wysłać to te pola i priorytet w formacie json, nie pisz nic innego poza rezultatem w formacie json, twoja wiadomość musi składać się tylko ze znaków które można zparsować na JSON, utrzymaj konsekwentnie następujący format: {\"propertyName\": priorityValue, \"propertyName\": priorityValue} - odpowiedź musi zawrzeć się tylko w jednym obiekcie, wartości priorytetów mogą być tylko z zakresu od 0 do 100 włącznie, dane podane są poniżej: ###\n"


Do testów wykorzystaliśmy 5 modeli:
"deepseek-ai/DeepSeek-V3-0324"
"moonshotai/Kimi-K2-Instruct-0905"
"openai/gpt-oss-20b:groq"
"CohereLabs/command-a-translate-08-2025:cohere"
"inclusionAI/Ling-1T:featherless-ai"



Testy dla każdej bazy danych powtórzyliśmy 3 razy.




Problemy:
W trakcie wykonania próbnego napotkaliśmy problem z modelem:
CohereLabs/command-a-translate-08-2025:cohere

openai.BadRequestError: Error code: 400 - {'id': 'ef1ad312-576b-4720-8cd4-4b1759942dac', 'message': 'too many tokens: size limit exceeded by 105000 tokens. Try using shorter or fewer inputs. The limit for this model is 8992 tokens.'}

Limit tokenów w jednej wiadomości został znacznie przekroczony.
W związku z tym zedytowaliśmy kod źródłowy i przeprowadziliśmy badania dla tego modelu tylko na bazie danych zawierającej 50 obiektów ("sampledb50.json")


jak również z modelem 
"inclusionAI/Ling-1T:featherless-ai"

2025-11-24 22:02:35 | INFO | _client.py:1025 >>> HTTP Request: POST https://router.huggingface.co/v1/chat/completions "HTTP/1.1 503 Service Temporarily Unavailable"

który odrzucał za pytania, najprawdopodobniej ze względu na przekroczenie limitu input tokenów

na temat modelu znaleźliśmy informację:
`Pre-trained on 20 trillion+ high-quality, reasoning-dense tokens, Ling-1T-base supports up to 128K context length`
która sugerowała by że na bazie danych `sampledb500.json` model wciąż powinien być w stanie wykonać kwerendę (miała ona 67300 tokenów), jednak api odrzucało zapytanie z kodem błędu HTTP 503 przy próbie wysłania bazy danych. W związku z tym również został pominięty w testach powyżej 200 obiektów.




Wyniki testów:



# ----------------------------------
# | TEST 1 - KWERENDA ZAAWANSOWANA |
# ----------------------------------

Test pierwszy - zaawansowana kwerenda
"query": "Znajdź dzieła wykonane w trakcie wojny w danym państwie"
# //TODO: Tu opis dlaczego jest zaawansowana, tzn. wymaga połączenia kilku cech, nie jest zapytaniem wprost, wymaga wiedzy z poza bazy danych na temat historii danego państwa i nie tylko, złączenie wielu cech może zapewnić odpowiedź o wysokim prawdopodobieństwie ale nie zawsze jednoznaczną, etc.


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
creator - imię i nazwisko autora, pozwala określić w jakich latach żył i na podstawie tego określić czy mógł wtedy trwać konflikt zbrojny

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



### Pierwszy test na bazie danych o ilości obiektów 50:

## Drugi test na bazie danych o ilości obiektów 50:

# Trzeci test na bazie danych o ilości obiektów 50:

# Podsumowanie testu na bazie danych o ilości obiektów 50:


!!!
Pominięto testy na modelu CohereLabs/command-a-translate-08-2025:cohere na większych bazach danych
ze względu na problemy z limitem kontekstu wspomiane na początku raportu.
!!!


### Pierwszy test na bazie danych o ilości obiektów 100:

## Drugi test na bazie danych o ilości obiektów 100:

# Trzeci test na bazie danych o ilości obiektów 100:

# Podsumowanie testu na bazie danych o ilości obiektów 100:

# //TODO PODSUMOWANIE


### Pierwszy test na bazie danych o ilości obiektów 200:

## Drugi test na bazie danych o ilości obiektów 200:

# Trzeci test na bazie danych o ilości obiektów 200:

# Podsumowanie testu na bazie danych o ilości obiektów 200:

# //TODO PODSUMOWANIE


### Pierwszy test na bazie danych o ilości obiektów 500:

## Drugi test na bazie danych o ilości obiektów 500:

# Trzeci test na bazie danych o ilości obiektów 500:

# Podsumowanie testu na bazie danych o ilości obiektów 500:

# //TODO PODSUMOWANIE


### Pierwszy test na bazie danych o ilości obiektów 959:

## Drugi test na bazie danych o ilości obiektów 959:

# Trzeci test na bazie danych o ilości obiektów 959:

# Podsumowanie testu na bazie danych o ilości obiektów 959:

# //TODO PODSUMOWANIE








### Podsumowanie wszystkich testów kwerendy średniozaawansowanej:
# //TODO PODSUMOWANIE





















# -------------------------------
# | TEST 3 - KWERENDA TRYWIALNA |
# -------------------------------


### Pierwszy test na bazie danych o ilości obiektów 50:

## Drugi test na bazie danych o ilości obiektów 50:

# Trzeci test na bazie danych o ilości obiektów 50:

# Podsumowanie testu na bazie danych o ilości obiektów 50:


!!!
Pominięto testy na modelu CohereLabs/command-a-translate-08-2025:cohere na większych bazach danych
ze względu na problemy z limitem kontekstu wspomiane na początku raportu.
!!!

### Pierwszy test na bazie danych o ilości obiektów 100:

## Drugi test na bazie danych o ilości obiektów 100:

# Trzeci test na bazie danych o ilości obiektów 100:

# Podsumowanie testu na bazie danych o ilości obiektów 100:

# //TODO PODSUMOWANIE


### Pierwszy test na bazie danych o ilości obiektów 200:

## Drugi test na bazie danych o ilości obiektów 200:

# Trzeci test na bazie danych o ilości obiektów 200:

# Podsumowanie testu na bazie danych o ilości obiektów 200:

# //TODO PODSUMOWANIE


### Pierwszy test na bazie danych o ilości obiektów 500:

## Drugi test na bazie danych o ilości obiektów 500:

# Trzeci test na bazie danych o ilości obiektów 500:

# Podsumowanie testu na bazie danych o ilości obiektów 500:

# //TODO PODSUMOWANIE


### Pierwszy test na bazie danych o ilości obiektów 959:

## Drugi test na bazie danych o ilości obiektów 959:

# Trzeci test na bazie danych o ilości obiektów 959:

# Podsumowanie testu na bazie danych o ilości obiektów 959:

# //TODO PODSUMOWANIE








### Podsumowanie wszystkich testów kwerendy trywialnej:
# //TODO PODSUMOWANIE






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
- Najtańszy: Llama-3.1-8B ($0.02/1M tokens)
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

# //TODO: Wnioski o limicie kontekstu, rozwiązanie - wysyłanie kilku zapytań z podzieloną bazą danych w zakresie kontekstu modelu
# //TODO: proponowane kolejne rozwiązanie (optymalizacja) na masywne ilości tokenów - wysłanie tylko unikalnych cech i unikalnych wartości odpowiadających tym cechom w bazie danych. problemy z tym rozwiązaniem - nie jest adekwatne dla każdej bazy danych, może powodować problemy z ustaleniem odpowiednich priorytetów (wymaga dalszych badań). Bazy danych które nie mają wielu unikatowych wartości mogą z tego skorzystać i wyjść bardzo efektywnie pod względem kosztów, ale bazy które mają wiele różnych wartości - nie będzie to ogromna optymalizacja.
# //TOOD: Wnioski o ilości czasu, czy to długie wykonanie, czy warto z tego korzystać, przewidywania jak się to będzie prezentowało na większych bazach danych (powyżej 200 000 tokenów)
# //TODO: Wady i zalety naszego rozwiązania







