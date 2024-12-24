import csv

def read_csv(path):
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        reader  = csv.DictReader(f)
        for row in reader:
            data.append({
                'product_id': int(row['product_id']),
                'name': row['name'],
                'price': float(row['price']),
                'quantity': int(row['quantity']),
                'category': row['category'], 
                'description': row['description'],
                'production_date': row['production_date'],
                'expiration_date': row['expiration_date'],
                #'rating': float(row['rating']), need to delete
                'status': row['status']
            })
    return data

data = read_csv('./4_task/fourth_task.txt')
size = len(data)
avg_price = 0
max_quantity = data[0]['quantity']
min_price = data[0]['price']

filtered_data = []

for item in data:
    avg_price += item['price']
    if max_quantity < item['quantity']:
        max_quantity = item['quantity']
    if min_price > item['price']:
        min_price = item['price']

    if item['category'] == 'Напитки':
        filtered_data.append(item)

avg_price /= size

with open('./4_task/fourth_task_avg_min_max_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"{avg_price}\n")
    f.write(f"{max_quantity}\n")
    f.write(f"{min_price}\n")


with open('./4_task/fourth_task_fitered_result.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, filtered_data[0].keys())
    writer.writeheader()
    for row in filtered_data:
        writer.writerow(row)