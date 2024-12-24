from bs4 import BeautifulSoup
import json

def handle_hard_file(path):

    with open(path, "r", encoding="utf-8") as file:
        html_context = file.read()

    soup = BeautifulSoup(html_context, "html.parser")

    build = soup.find_all("div", attrs = {"class", "mw-parser-output"})[0]
    item = {}
    item['Name'] = build.find_all("h2")[0].get_text()

    items = []
    for i in range(len(build.find_all("h4"))):
        info = {}
        info['Ancient One Name'] = build.find_all("h4")[i].get_text()
        mystery_table = build.find_all("table")[i].find_all("tbody")[0].find_all("tr")
        mysteries = []
        for j in mystery_table:
            mysteries_info = {}
            table_item = j.find_all("td")

            mysteries_info['Mystery Name'] = table_item[1].get_text().strip().replace("\n", "")
            mysteries_info['Mystery Type'] = table_item[2].get_text().strip().replace("\n", "")

            mysteries.append(mysteries_info)

        info['Mysteries'] = mysteries

        items.append(info)
    item['Ancient Ones'] = items


    investigators = build.find_all("ul")[0].find_all("li")
    items = []
    for i in investigators:
        items.append(i.get_text().strip().replace("\n", ""))
    item['Investigators'] = items

    counter = 0
    for i in range(len(build.find_all("h4")), len(build.find_all("table"))):
        assets_info = {}
        assets_table = build.find_all("table")[i].find_all("tbody")[0].find_all("tr")
        assets = []
        for j in assets_table:
            assets_info = {}
            table_item = j.find_all("td")
            #print(table_item)
            assets_info['Asset Name'] = table_item[1].get_text().strip().replace("\n", "")
            assets_info['Asset Trait'] = table_item[2].get_text().strip().replace("\n", "")
            assets_info['Asset Count'] = table_item[3].get_text().strip().replace("\n", "")

            assets.append(assets_info)
        
        if counter == 1:
            item['Unique_assets'] = assets
        else:
            item['Assets'] = assets

        counter += 1

    return item

def save_jsons(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def math_for_assets(data):
    assets = [item['Assets'] for item in data]
    numbers = []
    for i in assets:
        for j in i:
            numbers.append(int(j['Asset Count']))

    sum_assets = sum(numbers)
    min_assets = min(numbers)
    max_assets = max(numbers)
    avg_assets = sum_assets / len(numbers)

    statistics = {
        'sum': sum_assets,
        'min': min_assets,
        'max': max_assets,
        'avg': avg_assets
    }
    return statistics

def count_mystery_types(data):
    types_counts = {}
    for item in data:
        tag = item['Ancient Ones']
        for i in tag:
            for j in i['Mysteries']:
                if j['Mystery Type'] in types_counts:
                    types_counts[j['Mystery Type']] += 1
                else:
                    types_counts[j['Mystery Type']] = 1
    return types_counts

items = []
for i in range(4):
    items.append(handle_hard_file(f"./task_5/mult_objects_5/{i+1}.html"))

sorted_data = sorted(items, key=lambda x: len(x['Name']))
filtered_data = [item for item in items if len(item['Ancient Ones']) > 1]
statistics_data = math_for_assets(items)
frequency_data = count_mystery_types(items)

save_jsons('./task_5/mult_objects_5/result.json', items)
save_jsons('./task_5/mult_objects_5/sorted_data.json', sorted_data)
save_jsons('./task_5/mult_objects_5/filtered_data.json', filtered_data)
save_jsons('./task_5/mult_objects_5/statistics.json', statistics_data)
save_jsons('./task_5/mult_objects_5/frequency.json', frequency_data)