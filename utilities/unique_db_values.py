import json
from collections import defaultdict

with open('sampledb.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

unique_values = defaultdict(set)
unique_values_list = {} 

for record in data:
    for key, value in record.items():
        if value:  # Ignoruj puste wartości
            unique_values[key].add(value)

for key, values in unique_values.items():
    unique_values_list[key] = sorted(list(values))

statistics = {
    "total_records": len(data),
    "total_fields": len(unique_values),
    "fields_summary": {}
}

for key, values in unique_values.items():
    statistics["fields_summary"][key] = {
        "unique_count": len(values),
        "values": sorted(list(values))
    }

frequency_fields = ['creator', 'place', 'material', 'technique', 'type', 'copyright']
frequency_data = {}

for field in frequency_fields:
    if field in [key for key in data[0].keys()]:
        freq = defaultdict(int)
        for record in data:
            if record.get(field):
                freq[record[field]] += 1
        
        frequency_data[field] = [
            {"value": value, "count": count} 
            for value, count in sorted(freq.items(), key=lambda x: x[1], reverse=True)
        ]

output_data = {
    "statistics": statistics,
    "unique_values": unique_values_list,
    "frequency_analysis": frequency_data
}

with open('unique_values.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, ensure_ascii=False, indent=2)

print("✓ Wyniki zapisane do pliku: unique_values.json")


print("=" * 80)
print("ANALIZA UNIKALNYCH WARTOŚCI W BAZIE DANYCH FOTOGRAFII")
print("=" * 80)
print(f"\nŁączna liczba rekordów: {len(data)}")
print(f"Liczba cech: {len(unique_values)}")
print("\n" + "=" * 80)

for key, values in sorted(unique_values.items()):
    sorted_values = sorted(values)
    print(f"\n{key.upper()}")
    print("-" * 80)
    print(f"Liczba unikalnych wartości: {len(sorted_values)}")
    print("\nWartości:")
    for i, value in enumerate(sorted_values, 1):
        print(f"  {i}. {value}")

print("\n" + "=" * 80)
print("PODSUMOWANIE STATYSTYK")
print("=" * 80)

for key, values in sorted(unique_values.items()):
    print(f"{key:20} -> {len(values):4} unikalnych wartości")

print("\n" + "=" * 80)
print("NAJCZĘSTSZE WARTOŚCI (TOP 5 dla wybranych cech)")
print("=" * 80)

for field in frequency_fields:
    if field in frequency_data:
        print(f"\n{field.upper()}:")
        for item in frequency_data[field][:5]:
            print(f"  {item['value']:40} -> {item['count']:3} razy")

print("\n" + "=" * 80)
print("✓ Pełne wyniki zapisane do pliku: unique_values.json")
print("=" * 80)