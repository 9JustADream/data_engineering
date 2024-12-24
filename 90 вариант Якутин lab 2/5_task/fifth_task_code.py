import pandas as pd
import json
import msgpack
import pickle
import os

#Был выбран датасет https://www.kaggle.com/datasets/dansbecker/powerlifting-database
#Базовый размер датасета в формате csv 30 MB

file_path = r'C:\Users\admin\Downloads\data\openpowerlifting.csv'
df = pd.read_csv(file_path)

selected_columns = ['Sex', 'Equipment', 'Name', 'Age', 'BodyweightKg', 'BestBenchKg', 'BestDeadliftKg']
df_selected = df[selected_columns]

# Расчет характеристик для числовых данных
numeric_columns = df_selected.select_dtypes(include=['number']).columns
numeric_stats = {}
for col in numeric_columns:
    numeric_stats[col] = {
        'max': df_selected[col].dropna().max(),
        'min': df_selected[col].dropna().min(),
        'mean': df_selected[col].dropna().mean(),
        'sum': df_selected[col].dropna().sum(),
        'std': df_selected[col].dropna().std()
    }

# Расчет частоты встречаемости для текстовых данных
categorical_columns = df_selected.select_dtypes(include=['object']).columns
categorical_stats = {}
for col in categorical_columns:
    categorical_stats[col] = df_selected[col].dropna().value_counts().to_dict()

stats = {
    'numeric_stats': numeric_stats,
    'categorical_stats': categorical_stats
}
with open('./5_task/fifth_task_stats.json', 'w') as f:
    json.dump(stats, f, indent=4)


# Сохранение набора данных в разных форматах. Сохраняю в другую папку чтобы не отправлять несколько огромных датасетов в архиве
df_selected.to_csv(r'C:\Users\admin\Downloads\data\selected_data.csv', index=False)
df_selected.to_json(r'C:\Users\admin\Downloads\data\selected_data.json', orient='records', lines=True)
with open(r'C:\Users\admin\Downloads\data\selected_data.msgpack', 'wb') as f:
    f.write(msgpack.packb(df_selected.to_dict(orient='records')))
with open(r'C:\Users\admin\Downloads\data\selected_data.pkl', 'wb') as f:
    pickle.dump(df_selected, f)

# Сравнение размеров файлов
file_sizes = {
    'csv': os.path.getsize(r'C:\Users\admin\Downloads\data\selected_data.csv'),
    'json': os.path.getsize(r'C:\Users\admin\Downloads\data\selected_data.json'),
    'msgpack': os.path.getsize(r'C:\Users\admin\Downloads\data\selected_data.msgpack'),
    'pkl': os.path.getsize(r'C:\Users\admin\Downloads\data\selected_data.pkl')
}

with open('./5_task/fifth_task_file_sizes.txt', 'w') as f:
    for format, size in file_sizes.items():
        f.write(f"{format}: {size} bytes\n")