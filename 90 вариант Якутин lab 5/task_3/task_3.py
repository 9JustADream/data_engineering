import csv
import pymongo

def connect_db():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['db-202444']
    collection = db['jobs']
    return collection

def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='UTF-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            data.append(row)
    return data

# Чтение данных из CSV файла и добавление их в коллекцию
csv_data = read_csv('task_3/task_3_item.csv')
for item in csv_data:
    item['salary'] = float(item['salary'])
    item['age'] = int(item['age'])
connect_db().insert_many(csv_data)

# Удаление документов по предикату: salary < 25000 || salary > 175000
connect_db().delete_many({
    '$or': [
        {'salary': {'$lt': 25000}},
        {'salary': {'$gt': 175000}}
    ]
})

# Увеличение возраста (age) всех документов на 1
connect_db().update_many({}, {'$inc': {'age': 1}})

# Поднятие заработной платы на 5% для произвольно выбранных профессий
selected_jobs = ['Косметолог', 'Программист']
connect_db().update_many(
    {'job': {'$in': selected_jobs}},
    {'$mul': {'salary': 1.05}}
)

# Поднятие заработной платы на 7% для произвольно выбранных городов
selected_cities = ['Мадрид', 'Барселона']
connect_db().update_many(
    {'city': {'$in': selected_cities}},
    {'$mul': {'salary': 1.07}}
)

# Поднятие заработной платы на 10% для выборки по сложному предикату
complex_predicate = {
    'city': 'Монсон',
    'job': {'$in': ['Программист', 'Инженер']},
    'age': {'$gte': 30, '$lte': 45}
}
connect_db().update_many(
    complex_predicate,
    {'$mul': {'salary': 1.10}}
)

# Удаление записей по произвольному предикату
arbitrary_predicate = {
    'city': 'Семана',
    'job': 'Медсестра',
    'age': {'$lt': 30}
}
connect_db().delete_many(arbitrary_predicate)