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

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return f"File not found: {file_path}"

def create_songs_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE songs (id integer primary key, 
                   artist text,
                   song text, 
                   duration_ms integer,
                   year integer,
                   tempo real,
                   genre text,
                   popularity int)
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, popularity)
        VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre, :popularity)
    """, items)
    db.commit() 

def save_jsons(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def connect_to_db_dict(file):
    conn = sqlite3.connect(file) 
    conn.row_factory = sqlite3.Row
    return conn

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM songs
        ORDER BY popularity DESC
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
            SUM(duration_ms) as overall_duration,
            MIN(year) as min_year,
            MAX(year) as max_year,
            AVG(duration_ms) as avg_duration
        FROM songs
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
            artist
        FROM songs
        GROUP BY artist
        ORDER BY count DESC
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM songs
        WHERE tempo > 170
        ORDER BY popularity DESC
        LIMIT 105
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items


#STEP 1 DONE
#db = connect_to_db("task_1/first_db.db")
#create_songs_table(db)
#items_1 = read_json('task_3/3/_part_1.json')
#items_2 = read_pkl('task_3/3/_part_2.pkl')
#insert_data(db, items_1)
#insert_data(db, items_2)

#STEP 2
db = connect_to_db_dict("task_1/first_db.db")
save_jsons('task_3/first_q.json', first_query(db))
save_jsons('task_3/second_q.json', second_query(db))
save_jsons('task_3/third_q.json', third_query(db))
save_jsons('task_3/fourth_q.json', fourth_query(db))