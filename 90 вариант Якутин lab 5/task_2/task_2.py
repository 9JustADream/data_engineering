import json
import pymongo
import msgpack

def connect_db():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['db-202444']
    collection = db['jobs']
    return collection

def parse_data(file_path):
    with open(file_path, 'rb') as file:
        data = msgpack.unpackb(file.read(), raw=False)
    return data

def convert_to_json(value_to_convert, filename):
    with open(filename + '.json', 'w', encoding='UTF-8') as file:
        json.dump(value_to_convert, file, ensure_ascii=False)
    return

def count_mean(list_of_dicts):
    sum = 0
    key_name = list(list_of_dicts[0].keys())[0]
    for item in list_of_dicts:
        sum += item[key_name]
    mean = sum / len(list_of_dicts)
    return round(mean, 2)

connect_db().insert_many(parse_data('task_2/task_2_item.msgpack'))

# Вывод минимальной, средней, максимальной salary
min_salary = connect_db().find_one(sort=[('salary', 1)])['salary']
max_salary = connect_db().find_one(sort=[('salary', -1)])['salary']

all_salaries = list(connect_db().find({}, {'salary': True, '_id': False}))
mean_salary = count_mean(all_salaries)

answer_1 = {'min': min_salary, 'max': max_salary, 'mean': mean_salary}
convert_to_json(answer_1, 'task_2/answer_1')

# Вывод количества данных по представленным профессиям
job_counts = connect_db().aggregate([
    {'$group': {'_id': '$job', 'count': {'$sum': 1}}}
])
answer_2 = list(job_counts)
convert_to_json(answer_2, 'task_2/answer_2')

# Вывод минимальной, средней, максимальной salary по городу
pipeline = [
    {'$group': {'_id': '$city', 'min': {'$min': '$salary'}, 'max': {'$max': '$salary'}, 'avg': {'$avg': '$salary'}}}
]
salary_by_city = connect_db().aggregate(pipeline)
answer_3 = list(salary_by_city)
convert_to_json(answer_3, 'task_2/answer_3')

# Вывод минимальной, средней, максимальной salary по профессии
pipeline = [
    {'$group': {'_id': '$job', 'min': {'$min': '$salary'}, 'max': {'$max': '$salary'}, 'avg': {'$avg': '$salary'}}}
]
salary_by_job = connect_db().aggregate(pipeline)
answer_4 = list(salary_by_job)
convert_to_json(answer_4, 'task_2/answer_4')

# Вывод минимального, среднего, максимального возраста по городу
pipeline = [
    {'$group': {'_id': '$city', 'min': {'$min': '$age'}, 'max': {'$max': '$age'}, 'avg': {'$avg': '$age'}}}
]
age_by_city = connect_db().aggregate(pipeline)
answer_5 = list(age_by_city)
convert_to_json(answer_5, 'task_2/answer_5')

# Вывод минимального, среднего, максимального возраста по профессии
pipeline = [
    {'$group': {'_id': '$job', 'min': {'$min': '$age'}, 'max': {'$max': '$age'}, 'avg': {'$avg': '$age'}}}
]
age_by_job = connect_db().aggregate(pipeline)
answer_6 = list(age_by_job)
convert_to_json(answer_6, 'task_2/answer_6')

# Вывод максимальной заработной платы при минимальном возрасте
max_salary_min_age = connect_db().find_one(sort=[('age', 1), ('salary', -1)])
answer_7 = {'age': max_salary_min_age['age'], 'salary': max_salary_min_age['salary']}
convert_to_json(answer_7, 'task_2/answer_7')

# Вывод минимальной заработной платы при максимальном возрасте
min_salary_max_age = connect_db().find_one(sort=[('age', -1), ('salary', 1)])
answer_8 = {'age': min_salary_max_age['age'], 'salary': min_salary_max_age['salary']}
convert_to_json(answer_8, 'task_2/answer_8')

# Вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50000, отсортировать вывод по убыванию по полю avg
pipeline = [
    {'$match': {'salary': {'$gt': 50000}}},
    {'$group': {'_id': '$city', 'min': {'$min': '$age'}, 'max': {'$max': '$age'}, 'avg': {'$avg': '$age'}}},
    {'$sort': {'avg': -1}}
]
age_by_city_salary = connect_db().aggregate(pipeline)
answer_9 = list(age_by_city_salary)
convert_to_json(answer_9, 'task_2/answer_9')

# Вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту: 18<age<25 & 50<age<65
pipeline = [
    {'$match': {
        '$and': [
            {'city': 'Тарраса'},
            {'job': 'Повар'},
            {'$or': [
                {'$and': [{'age': {'$gt': 18}}, {'age': {'$lt': 25}}]},
                {'$and': [{'age': {'$gt': 50}}, {'age': {'$lt': 65}}]}
            ]}
        ]
    }},
    {'$group': {
        '_id': {'city': '$city', 'job': '$job'},
        'min': {'$min': '$salary'},
        'max': {'$max': '$salary'},
        'avg': {'$avg': '$salary'}
    }}
]
salary_in_ranges = connect_db().aggregate(pipeline)
answer_10 = list(salary_in_ranges)
convert_to_json(answer_10, 'task_2/answer_10')

# Произвольный запрос с $match, $group, $sort
# Вычисление средней заработной платы для каждой группы профессий, среди заработных плат больше 30000 
pipeline = [
    {'$match': {'salary': {'$gt': 30000}}},
    {'$group': {'_id': '$job', 'avg_salary': {'$avg': '$salary'}}},
    {'$sort': {'avg_salary': -1}}
]
custom_query = connect_db().aggregate(pipeline)
answer_11 = list(custom_query)
convert_to_json(answer_11, 'task_2/answer_11')