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

def create_prise_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE price (id integer primary key, 
                   tournament_name text references tournament(name),
                   place integer, 
                   prise integer)
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO price (tournament_name, place, prise)
        VALUES (:name, :place, :prise)
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
        FROM price
        WHERE tournament_name = 'Кубок мира 1969'
        ORDER BY place
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT t.name, t.id, p.prise
        FROM tournament t
        JOIN price p ON t.name = p.tournament_name
        WHERE p.place = 0
        LIMIT 10
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT t.name, sum(p.prise) as prise_found, max(p.place) as place_count
        FROM tournament t
        JOIN price p ON t.name = p.tournament_name
        GROUP BY t.name
        ORDER BY prise_found DESC
        LIMIT 10
    """)

    items = []
    for row in res.fetchall():
        items.append(dict(row))

    return items

#STEP 1 DONE
#db = connect_to_db("task_1/first_db.db")
#create_prise_table(db)
#items = read_pkl('task_1/1-2/subitem.pkl')
#insert_data(db, items)

#STEP 2
db = connect_to_db_dict("task_1/first_db.db")
save_jsons('task_2/first_q.json', first_query(db))
save_jsons('task_2/second_q.json', second_query(db))
save_jsons('task_2/third_q.json', third_query(db))