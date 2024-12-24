from bs4 import BeautifulSoup
import json

def handle_easy_file(path):

    with open(path, "r", encoding="utf-8") as file:
        html_context = file.read()

    soup = BeautifulSoup(html_context, "html.parser")

    build = soup.find_all("div", attrs = {"class", "mw-parser-output"})[0]
    item = {}

    first_table = build.find_all("table")[0].find_all("tr")
    for i in first_table:
        table_item = i.get_text().strip().replace("\n", "").split(':')

        if len(table_item[0]) == 0:
            item['Reckoning'] = table_item[1]
        else:
            item[table_item[0]] = table_item[1]

    second_table = build.find_all("table")[1].find_all("tr")
    for i in second_table:
        table_item = i.get_text().strip().replace("\n", "").split(':')

        if table_item[1] != 'N/A' and table_item[1] != 'No':
            if len(table_item[0]) == 0:
                item['Reckoning_text'] = table_item[1].replace("  ", " ")
            else:
                item[f'{table_item[0]}_text'] = table_item[1].replace("  ", " ")

    item['Variants'] = int(item['Variants'])

    return item

def save_jsons(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def math_for_variants(data):
    variants = [item['Variants'] for item in data]

    sum_variants = sum(variants)
    min_variants = min(variants)
    max_variants = max(variants)
    avg_variants = sum_variants / len(variants)

    statistics = {
        'sum': sum_variants,
        'min': min_variants,
        'max': max_variants,
        'avg': avg_variants
    }
    return statistics

def count_tags(data):
    tags_counts = {}
    for item in data:
        tag = item['Tags']
        if tag in tags_counts:
            tags_counts[tag] += 1
        else:
            tags_counts[tag] = 1
    return tags_counts

items = []
for i in range(12):
    items.append(handle_easy_file(f"./task_5/one_object_5/{i+1}.html"))

sorted_data = sorted(items, key=lambda x: len(x['Name']))
filtered_data = [item for item in items if item['Reckoning'] == 'Yes']
statistics_data = math_for_variants(items)
frequency_data = count_tags(items)

save_jsons('./task_5/one_object_5/result.json', items)
save_jsons('./task_5/one_object_5/sorted_data.json', sorted_data)
save_jsons('./task_5/one_object_5/filtered_data.json', filtered_data)
save_jsons('./task_5/one_object_5/statistics.json', statistics_data)
save_jsons('./task_5/one_object_5/frequency.json', frequency_data)