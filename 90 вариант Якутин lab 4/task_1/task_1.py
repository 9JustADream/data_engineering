import sqlite3
import pickle
import json

def connect_to_db(file):
    return sqlite3.connect(file)

def read_pkl(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def create_tournament_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE tournament (id integer primary key, 
                   name text, 
                   city text, 
                   begin text, 
                   system text, 
                   tours_count integer, 
                   min_rating integer, 
                   time_on_game integer)
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO tournament (id, name, city, begin, system, tours_count, min_rating, time_on_game)
        VALUES (:id, :name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)
    """, items)
    db.commit() 

def connect_to_db_dict(file):
    conn = sqlite3.connect(file) 
    conn.row_factory = sqlite3.Row
    return conn

def save_jsons(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM tournament
        ORDER BY min_rating
        LIMIT 100
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            COUNT(*) as tournaments_count,
            MIN(tours_count) as min_tours_count,
            MAX(tours_count) as max_tours_count,
            AVG(min_rating) as avg_min_rating
        FROM tournament
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items[0]

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            COUNT(*) as count,
            system
        FROM tournament
        GROUP BY system
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM tournament
        WHERE min_rating < 2300
        ORDER BY min_rating DESC
        LIMIT 100
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

#STEP 1 DONE
#create_tournament_table(connect_to_db("task_1/first_db.db"))
#items = read_pkl('task_1/1-2/item.pkl')
#db = connect_to_db("task_1/first_db.db")
#insert_data(db, items)

#STEP 2
db = connect_to_db_dict("task_1/first_db.db")
save_jsons('task_1/first_q.json', first_query(db))
save_jsons('task_1/second_q.json', second_query(db))
save_jsons('task_1/third_q.json', third_query(db))
save_jsons('task_1/fourth_q.json', fourth_query(db))