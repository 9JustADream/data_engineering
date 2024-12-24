import json
import pymongo
import csv

#STEP 1 INSERT DATA
def connect_to_collection(collection_name):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['db-202444']
    collection = db[collection_name]
    return collection

with open('task_4/music.json', 'r', encoding='UTF-8') as file:
    music_data = json.load(file)
connect_to_collection('music').insert_many(music_data)

def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='UTF-8') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    return data

csv_file_path = 'task_4/shopping_trends.csv'
shopping_data = read_csv(csv_file_path)

for item in shopping_data:
    item['Age'] = int(item['Age'])
    item['Purchase Amount (USD)'] = float(item['Purchase Amount (USD)'])
    item['Review Rating'] = float(item['Review Rating'])
    item['Previous Purchases'] = int(item['Previous Purchases'])

connect_to_collection('shopping_trends').insert_many(shopping_data)

def convert_to_json(value_to_convert, filename):
    with open('task_4/' + filename + '.json', 'w', encoding='UTF-8') as file:
        json.dump(value_to_convert, file, ensure_ascii=False)
    return

#STEP 2 TASKS
#TASK 1
danceable_tracks = list(connect_to_collection('music').find({'danceability': {'$gt': 0.7}}, projection={"_id": False}))
convert_to_json(danceable_tracks, 'selection_1')


california_purchases = list(connect_to_collection('shopping_trends').find({'Location': 'Massachusetts'}, projection={"_id": False}))
convert_to_json(california_purchases, 'selection_2')


high_energy_valence_tracks = list(connect_to_collection('music').find({
    '$and': [
        {'energy': {'$gt': 0.8}},
        {'valence': {'$gt': 0.6}}
    ]
}, projection={"_id": False}))
convert_to_json(high_energy_valence_tracks, 'selection_3')


older_female_purchases = list(connect_to_collection('shopping_trends').find({
    '$and': [
        {'Gender': 'Female'},
        {'Age': {'$gt': 40}}
    ]
}, projection={"_id": False}))
convert_to_json(older_female_purchases, 'selection_4')


fast_loud_tracks = list(connect_to_collection('music').find({
    '$and': [
        {'tempo': {'$gt': 120}},
        {'loudness': {'$lt': -5}}
    ]
}, projection={"_id": False}))
convert_to_json(fast_loud_tracks, 'selection_5')

#TASK 2
avg_danceability = list(connect_to_collection('music').aggregate([
    {'$group': {'_id': None, 'avg_danceability': {'$avg': '$danceability'}}},
    {'$project': {'_id': False}}
]))
convert_to_json(avg_danceability, 'aggregation_1')


avg_purchase_by_state = list(connect_to_collection('shopping_trends').aggregate([
    {'$group': {'_id': '$Location', 'avg_purchase': {'$avg': {'$toDouble': '$Purchase Amount (USD)'}}}}
]))
convert_to_json(avg_purchase_by_state, 'aggregation_2')


liked_tracks_count = list(connect_to_collection('music').aggregate([
    {'$match': {'liked': 1}},
    {'$count': 'liked_tracks_count'},
    {'$project': {'_id': False}}
]))
convert_to_json(liked_tracks_count, 'aggregation_3')


avg_review_rating_by_state = list(connect_to_collection('shopping_trends').aggregate([
    {'$group': {'_id': '$Location', 'avg_review_rating': {'$avg': {'$toDouble': '$Review Rating'}}}}
]))
convert_to_json(avg_review_rating_by_state, 'aggregation_4')


avg_energy_mode_1 = list(connect_to_collection('music').aggregate([
    {'$match': {'mode': 1}},
    {'$group': {'_id': None, 'avg_energy': {'$avg': '$energy'}}},
    {'$project': {'_id': False}}
]))
convert_to_json(avg_energy_mode_1, 'aggregation_5')

#TASK 3
connect_to_collection('music').update_many({}, {'$inc': {'danceability': 0.1}})
updated_tracks = list(connect_to_collection('music').find({}, projection={"_id": False}))
convert_to_json(updated_tracks, 'update_delete_1')


connect_to_collection('shopping_trends').delete_many({'Location': 'New York'})
remaining_purchases = list(connect_to_collection('shopping_trends').find({}, projection={"_id": False}))
convert_to_json(remaining_purchases, 'update_delete_2')


connect_to_collection('music').update_many({'liked': 0}, {'$inc': {'loudness': -1}})
updated_tracks = list(connect_to_collection('music').find({}, projection={"_id": False}))
convert_to_json(updated_tracks, 'update_delete_3')


connect_to_collection('shopping_trends').delete_many({
    '$and': [
        {'Gender': 'Male'},
        {'Age': {'$gt': 50}}
    ]
})
remaining_purchases = list(connect_to_collection('shopping_trends').find({}, projection={"_id": False}))
convert_to_json(remaining_purchases, 'update_delete_4')


connect_to_collection('music').update_many({'valence': {'$gt': 0.7}}, {'$inc': {'tempo': 5}})
updated_tracks = list(connect_to_collection('music').find({}, projection={"_id": False}))
convert_to_json(updated_tracks, 'update_delete_5')