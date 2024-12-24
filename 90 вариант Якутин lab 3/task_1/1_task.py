from bs4 import BeautifulSoup
import json

def handle_file(path):

    with open(path, "r", encoding="utf-8") as file:
        html_context = file.read()

    soup = BeautifulSoup(html_context, "html.parser")

    build = soup.find_all("div", attrs = {"class", "build-wrapper"})[0]
    item = {}
    item['city'] = build.find_all("span")[0].get_text().split(":")[1].strip()
    item['id'] = int(build.h1['id'])
    item['type'] = build.h1.get_text().split(":")[1].strip()
    address_temp = build.p.get_text().strip().replace("\n", "")
    address_temp = address_temp.split("Улица: ")[1].split("Индекс:")
    item['adress'] = address_temp[0].strip()
    item['index'] = address_temp[1].strip()
    item['floors'] = int(build.find_all('span', attrs = {"class": "floors"})[0].get_text().split(":")[1])
    item['year'] = int(build.find_all('span', attrs = {"class": "year"})[0].get_text().split("Построено в")[1])
    spans = build.find_all('span', attrs = {"class": ""})
    item['parking'] = spans[1].get_text().split(":") == 'да'
    item['rating'] = float(spans[2].get_text().split(":")[1])
    item['views'] = int(spans[3].get_text().split(":")[1])
    item['img'] = build.img['src']

    return item

def save_jsons(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def math_for_views(data):
    views = [item['views'] for item in data]

    sum_views = sum(views)
    min_views = min(views)
    max_views = max(views)
    avg_views = sum_views / len(views)

    statistics = {
        'sum': sum_views,
        'min': min_views,
        'max': max_views,
        'avg': avg_views
    }
    return statistics

def count_city(data):
    city_counts = {}
    for item in data:
        city = item['city']
        if city in city_counts:
            city_counts[city] += 1
        else:
            city_counts[city] = 1
    return city_counts

items = []
for i in range(1,92):
    items.append(handle_file(f"./task_1/1/{i+1}.html"))

sorted_data = sorted(items, key=lambda x: x['year'])
filtered_data = [item for item in items if item['floors'] > 7]
statistics_data = math_for_views(items)
frequency_data = count_city(items)

save_jsons('./task_1/result.json', items)
save_jsons('./task_1/sorted_data.json', sorted_data)
save_jsons('./task_1/filtered_data.json', filtered_data)
save_jsons('./task_1/statistics.json', statistics_data)
save_jsons('./task_1/frequency.json', frequency_data)


