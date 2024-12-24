from bs4 import BeautifulSoup
import json

def handle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        xml_context = file.read()
    
    clothings = BeautifulSoup(xml_context, "xml").find_all("clothing")
    items = []
    for clothing in clothings:
        item = {}
        item["id"] = int(clothing.id.get_text())
        item["name"] = clothing.find_all('name')[0].get_text().strip()
        item["category"] = clothing.category.get_text().strip()
        item["size"] = clothing.size.get_text().strip()
        item["color"] = clothing.color.get_text().strip()
        item["material"] = clothing.material.get_text().strip()
        item["price"] = float(clothing.price.get_text().strip())
        item["rating"] = float(clothing.rating.get_text().strip())
        item["reviews"] = int(clothing.reviews.get_text().strip())
        if clothing.sporty is not None:
            item["sporty"] = clothing.sporty.get_text().strip() == "yes"
        if clothing.new is not None:
            item["new"] = clothing.new.get_text().strip() == "+"
        if clothing.exclusive is not None:
            item["exclusive"] = clothing.exclusive.get_text().strip() == "yes"
        
        items.append(item)
    
    return items

def save_jsons(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def math_for_reviews(data):
    reviews = [item['reviews'] for item in data]

    sum_reviews = sum(reviews)
    min_reviews = min(reviews)
    max_reviews = max(reviews)
    avg_reviews = sum_reviews / len(reviews)

    statistics = {
        'sum': sum_reviews,
        'min': min_reviews,
        'max': max_reviews,
        'avg': avg_reviews
    }
    return statistics

def count_material(data):
    material_counts = {}

    for item in data:
        material = item.get('material', 'Unknown')
        if material in material_counts:
            material_counts[material] += 1
        else:
            material_counts[material] = 1
    return material_counts

rew_items = []
for i in range(128):
    rew_items.append(handle_file(f"./task_4/4/{i+1}.xml"))
items = [item for sublist in rew_items for item in sublist]

sorted_data = sorted(items, key=lambda x: x['price'])
filtered_data = [item for item in items if item['rating'] > 4.5]
statistics_data = math_for_reviews(items)
frequency_data = count_material(items)

save_jsons('./task_4/result.json', items)
save_jsons('./task_4/sorted_data.json', sorted_data)
save_jsons('./task_4/filtered_data.json', filtered_data)
save_jsons('./task_4/statistics.json', statistics_data)
save_jsons('./task_4/frequency.json', frequency_data)
