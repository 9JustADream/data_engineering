import pymongo
import json

def connect_db():

    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['db-202444']
    collection = db['jobs']
    return collection

def parse_data(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def convert_to_json(value_to_convert, filename):
    with open(filename + '.json', 'w', encoding='UTF-8') as file:
        json.dump(value_to_convert, file, ensure_ascii=False)
    return

connect_db().insert_many(parse_data('task_1/task_1_item.json'))

query_1 = list(connect_db().find(filter={},
                                            sort=[('salary', -1)],
                                            limit=10,
                                            projection={"_id": False}))
convert_to_json(query_1, 'task_1/answer_1')

query_2 = list(connect_db().find(filter={'age': {'$lt': 30}},
                                            sort=[('salary', -1)],
                                            limit=15,
                                            projection={"_id": False}))
convert_to_json(query_2, 'task_1/answer_2')

query_3 = list(connect_db().find(filter={'city': 'Таллин',
                                                    'job': {'$in': ['Бухгалтер', 'Программист', 'Продавец']}},
                                            sort=[('age', 1)],
                                            limit=10,
                                            projection={"_id": False}))
convert_to_json(query_3, 'task_1/answer_3')

query_4_count = connect_db().count_documents(filter={
    '$and': [
        {'age': {'$gt': 20}},
        {'age': {'$lt': 30}},
        {'year': {'$gte': 2019, '$lte': 2022}},
        {'$or': [
            {'salary': {'$gt': 50000, '$lte': 75000}},
            {'salary': {'$gt': 125000, '$lt': 150000}}
        ]}
    ]
})
convert_to_json(query_4_count, 'task_1/answer_4')