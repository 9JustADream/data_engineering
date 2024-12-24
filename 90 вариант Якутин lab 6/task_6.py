import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder
import numpy as np

# https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets?select=transactions_data.csv
# Функция для анализа памяти
def memory_cal(data_file, dataset):
    file_size = os.path.getsize(data_file)
    print(f'Объем памяти, который занимает файл на диске: {file_size // 1024:10} КБ')
    memory_usage_stat = dataset.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    print(f'Объем памяти, который занимает набор данных при загрузке в память: {total_memory_usage // 1024:10} КБ')
    column_stat = []
    for key in dataset.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs": memory_usage_stat[key] // 1024,
            "memory_per": round(memory_usage_stat[key] / total_memory_usage * 100, 4),
            "dtype": str(dataset.dtypes[key])
        })
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    for column in column_stat:
        print(f"{column['column_name']:30}: {column['memory_abs']:10}КБ: {column['memory_per']:10}% : {column['dtype']}")
    return column_stat

# Функция для записи в JSON
def write_to_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4, default=str)

# Функция для преобразования объектов в категориальные
def col_category(dataset):
    converted_columns = {}
    for col in dataset.select_dtypes(include=['object']).columns:
        if dataset[col].nunique() / len(dataset) < 0.5:
            converted_columns[col] = dataset[col].astype('category')
    return pd.DataFrame(converted_columns)

# Функция для понижающего преобразования типов int
def col_num_int(dataset):
    converted_columns = {}
    for col in dataset.select_dtypes(include=['int']).columns:
        if dataset[col].min() >= np.iinfo(np.int8).min and dataset[col].max() <= np.iinfo(np.int8).max:
            converted_columns[col] = dataset[col].astype(np.int8)
        elif dataset[col].min() >= np.iinfo(np.int16).min and dataset[col].max() <= np.iinfo(np.int16).max:
            converted_columns[col] = dataset[col].astype(np.int16)
        elif dataset[col].min() >= np.iinfo(np.int32).min and dataset[col].max() <= np.iinfo(np.int32).max:
            converted_columns[col] = dataset[col].astype(np.int32)
        else:
            converted_columns[col] = dataset[col].astype(np.int64)
    return pd.DataFrame(converted_columns)

# Функция для понижающего преобразования типов float
def col_num_float(dataset):
    converted_columns = {}
    for col in dataset.select_dtypes(include=['float']).columns:
        if dataset[col].min() >= np.finfo(np.float16).min and dataset[col].max() <= np.finfo(np.float16).max:
            converted_columns[col] = dataset[col].astype(np.float16)
        elif dataset[col].min() >= np.finfo(np.float32).min and dataset[col].max() <= np.finfo(np.float32).max:
            converted_columns[col] = dataset[col].astype(np.float32)
        else:
            converted_columns[col] = dataset[col].astype(np.float64)
    return pd.DataFrame(converted_columns)

# Функция для чтения типов данных из JSON
def read_types(file_name):
    dtypes = {}
    with open(file_name, mode='r') as file:
        dtypes = json.load(file)
    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype
        else:
            dtypes[key] = np.dtype(dtypes[key])
    return dtypes

# Функция для преобразования категориальных признаков в числовые
def transform_category(dataset):
    cat_columns = []
    num_columns = []
    for column_name in dataset.columns:
        if isinstance(dataset[column_name].dtype, pd.CategoricalDtype):
            cat_columns.append(column_name)
        else:
            num_columns.append(column_name)
    ordinal = OrdinalEncoder()
    ordinal.fit(dataset[cat_columns])
    ordinal_encoded = ordinal.transform(dataset[cat_columns])
    df_ordinal = pd.DataFrame(ordinal_encoded, columns=cat_columns)
    df = pd.concat([dataset[num_columns], df_ordinal], axis=1)
    return df

# Функции для построения графиков
def figure_1(dataset):
    aggregated_data = dataset.groupby('merchant_state').agg({'amount': 'mean'}).reset_index()
    plt.figure(figsize=(20, 8))  # Увеличиваем размер графика
    sns.barplot(data=aggregated_data, x='merchant_state', y='amount', orient='v')
    plt.xticks(rotation=45, ha='right')  # Поворачиваем метки на оси X на 45 градусов
    plt.title('Bar Plot of merchant_state and average amount')
    plt.savefig('6_1_barplot.png')
    plt.close()
    print('1')


def figure_2(dataset):
    aggregated_data = dataset.groupby('use_chip').size().reset_index(name='count')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=aggregated_data, x='count', y='use_chip', orient='h')
    plt.title('Bar Plot of use_chip and count')
    plt.savefig('6_2_barplot_group.png')
    plt.close()
    print('2')

def figure_3(dataset):
    correlation_matrix = dataset.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig('6_3_heatmap.png')
    plt.close()
    print('3')

def figure_4(dataset):
    aggregated_data = dataset.groupby('client_id').agg({'amount': 'mean'}).reset_index()
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=aggregated_data, x='client_id', y='amount')
    plt.title('Scatter Plot of client_id and mean amount')
    plt.savefig('6_4_amount.png')
    plt.close()
    print('4')

def figure_5(dataset):
    merchant_state_counts = dataset['merchant_state'].value_counts().reset_index()
    merchant_state_counts.columns = ['merchant_state', 'count']
    total_counts = merchant_state_counts['count'].sum()
    threshold = 0.025 * total_counts
    other_states = merchant_state_counts[merchant_state_counts['count'] < threshold]
    other_count = other_states['count'].sum()
    other_label = f'other_{len(other_states)}_states'

    filtered_counts = merchant_state_counts[merchant_state_counts['count'] >= threshold]
    other_row = pd.DataFrame({'merchant_state': [other_label], 'count': [other_count]})
    filtered_counts = pd.concat([filtered_counts, other_row], ignore_index=True)

    plt.figure(figsize=(10, 6))
    plt.pie(filtered_counts['count'], labels=filtered_counts['merchant_state'], autopct='%1.1f%%')
    plt.title('Pie Chart of merchant_state')
    plt.savefig('6_5_show.png')
    plt.close()
    print('5')

file_name = 'transactions_data.csv'
statistic_json = 'statistic.json'
statistic_clear_json = 'statistic_clear.json'
colums_names = ['id', 'client_id', 'card_id', 'amount', 'use_chip', 'merchant_id', 'merchant_city', 'merchant_state', 'zip', 'mcc']
type_format = 'dtypes.json'
new_dataset = 'new_dataset.csv'

df = pd.read_csv(file_name)

# Анализ памяти и сохранение статистики
column_stat = memory_cal(file_name, df)
write_to_json(column_stat, statistic_json)

# Преобразование типов данных
converted_odj = col_category(df)
converted_int = col_num_int(df)
converted_float = col_num_float(df)

# Применение преобразований
optimized_dataset = df.copy()
optimized_dataset[converted_odj.columns] = converted_odj
optimized_dataset[converted_int.columns] = converted_int
optimized_dataset[converted_float.columns] = converted_float

# Повторный анализ памяти и сохранение статистики
column_stat_clear = memory_cal(file_name, optimized_dataset)
write_to_json(column_stat_clear, statistic_clear_json)

# Сохранение типов данных в JSON
opt_dtypes = optimized_dataset.dtypes
need_colum = {}
for key in colums_names:
    need_colum[key] = str(opt_dtypes[key])

with open(type_format, mode="w") as file:
    json.dump(need_colum, file, indent=4)

# Сохранение поднабора данных
has_header = True
for chunk in pd.read_csv(file_name,
                         usecols=lambda x: x in colums_names,
                         dtype=need_colum,
                         chunksize=100_000):
    chunk.to_csv(new_dataset, mode="a", header=has_header, index=False)
    has_header = False

# Чтение оптимизированного набора данных
need_dtypes = read_types(type_format)

total_rows = sum(1 for line in open(new_dataset)) - 1  # Подсчет общего количества строк
rows_to_read = total_rows // 20  # Определение количества строк для чтения

dataset = pd.read_csv(new_dataset, usecols=lambda x: x in need_dtypes.keys(), dtype=need_dtypes, nrows=rows_to_read)

# Преобразование категориальных признаков в числовые
df = transform_category(dataset)

# Построение графиков
figure_1(df)
figure_2(df)
figure_3(df)
figure_4(df)
figure_5(dataset)