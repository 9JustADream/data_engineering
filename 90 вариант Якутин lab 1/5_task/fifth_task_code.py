from bs4 import BeautifulSoup
import csv

with open('./5_task/fifth_task.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
columns = ["product_id","name","price","quantity","category","description",
           "production_date","expiration_date","rating","status"]

data = []

for row in soup.find_all("tr"):
    cols = row.find_all("td")
    item = {}
    column_index = 0
    for col in cols:
        val = col.get_text(strip=True)
        curr_column = columns[column_index]
        column_index += 1
        item[curr_column] = val
    if len(item) > 0:
        data.append(item)

with open('./5_task/fifth_task_result.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, data[0].keys())
    writer.writeheader()
    for row in data:
        writer.writerow(row)