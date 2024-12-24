from bs4 import BeautifulSoup
import json

def handle_file(path):

    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    products = soup.find_all("div", attrs = {"class", "product-item"})
    items = []

    for product in products:

        item = {}
        item['id'] = int(product.a['data-id'])
        item['link'] = product.find_all('a')[1]['href']
        item['img'] = product.img['src']
        item['title'] = product.span.get_text().strip()
        item['price'] = int(product.price.get_text().replace('₽', '').replace(' ', '').strip())
        item['bonus'] = int(product.strong.get_text().replace("+ начислим", '').replace(" бонусов", '').strip())

        prorepties = product.ul.find_all('li')
        for prop in prorepties:
            item[prop['type']] = prop.get_text().strip()

        items.append(item)
    
    return items

def save_jsons(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def math_for_price(data):
    prices = [item['price'] for item in data]

    sum_prices = sum(prices)
    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum_prices / len(prices)

    statistics = {
        'sum': sum_prices,
        'min': min_price,
        'max': max_price,
        'avg': avg_price
    }
    return statistics

def count_matrix(data):
    matrix_counts = {}

    for item in data:
        matrix = item.get('matrix', 'Unknown')
        if matrix in matrix_counts:
            matrix_counts[matrix] += 1
        else:
            matrix_counts[matrix] = 1
    return matrix_counts

rew_items = []
for i in range(65):
    rew_items.append(handle_file(f"./task_2/2/{i+1}.html"))
items = [item for sublist in rew_items for item in sublist]


sorted_data = sorted(items, key=lambda x: x['price'])
filtered_data = [item for item in items if item['bonus'] > 2000]
statistics_data = math_for_price(items)
frequency_data = count_matrix(items)

save_jsons('./task_2/result.json', items)
save_jsons('./task_2/sorted_data.json', sorted_data)
save_jsons('./task_2/filtered_data.json', filtered_data)
save_jsons('./task_2/statistics.json', statistics_data)
save_jsons('./task_2/frequency.json', frequency_data)