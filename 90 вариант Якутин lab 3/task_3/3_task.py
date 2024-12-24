from bs4 import BeautifulSoup
import json

def handle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        xml_context = file.read()
    
    star = BeautifulSoup(xml_context, "xml").star
    item = {}
    for el in star:
        if el.name is None:
            continue
        item[el.name] = el.get_text().strip()

    item['radius'] = int(item['radius'])
    return(item)

def save_jsons(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def math_for_radius(data):
    radii = [item['radius'] for item in data]

    sum_radius = sum(radii)
    min_radius = min(radii)
    max_radius = max(radii)
    avg_radius = sum_radius / len(radii)

    statistics = {
        'sum': sum_radius,
        'min': min_radius,
        'max': max_radius,
        'avg': avg_radius
    }
    return statistics

def count_constellation(data):
    constellation_counts = {}

    for item in data:
        constellation = item.get('constellation', 'Unknown')
        if constellation in constellation_counts:
            constellation_counts[constellation] += 1
        else:
            constellation_counts[constellation] = 1
    return constellation_counts

items = []
for i in range(149):
    items.append(handle_file(f"./task_3/3/{i+1}.xml"))

sorted_data = sorted(items, key=lambda x: x['radius'])
filtered_data = [item for item in items if float(item['age'].split()[0]) < 1]
statistics_data = math_for_radius(items)
frequency_data = count_constellation(items)

save_jsons('./task_3/result.json', items)
save_jsons('./task_3/sorted_data.json', sorted_data)
save_jsons('./task_3/filtered_data.json', filtered_data)
save_jsons('./task_3/statistics.json', statistics_data)
save_jsons('./task_3/frequency.json', frequency_data)