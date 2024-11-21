import hashlib
import pandas as pd
import requests  # или MongoDB клиент для работы с бд

# функция для хэширования значений с солью
def anonymize_value(value, salt):
    if pd.isna(value):
        return value  # не изменяем пустые значения
    return hashlib.sha256((salt + str(value)).encode()).hexdigest()

# функция для получения данных по ID (например, esia_id, event_id, RRN..)
def fetch_data_by_id(api_url, id_value, data_type):
    """
    Запрос к API (или бд) для получения данных по ID (например, esia_id, event_id, RRN).
    data_type: тип данных, которые нужно получить (например, 'transactions', 'events', 'tickets').
    """
    response = requests.get(f"{api_url}/{data_type}/{id_value}")
    if response.status_code == 200:
        return response.json()  # возвращаем данные в JSON
    else:
        return None  # ксли данные не найдены

# загрузка данных
def load_data(file_path, file_type='csv'):
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type == 'json':
        return pd.read_json(file_path)
    else:
        raise ValueError("Поддерживаются только форматы CSV и JSON")

# сохранение 
def save_data(dataframe, output_path, file_type='csv'):
    if file_type == 'csv':
        dataframe.to_csv(output_path, index=False)
    elif file_type == 'json':
        dataframe.to_json(output_path, orient='records', lines=True)
    else:
        raise ValueError("Поддерживаются только форматы CSV и JSON")

# основная функция для обезличивания и сбора данных
def anonymize_and_fetch_data(dataframe, columns_to_anonymize, salt, user_id_column, api_url):
    """
    Обезличивает данные и запрашивает связанные данные по ID (например, esia_id, event_id, RRN).
    """
    # хэширование айди пользователя (esia_id) с солью
    dataframe[user_id_column] = dataframe[user_id_column].apply(lambda x: anonymize_value(x, salt))

    # обезличиваем другие указанные столбцы
    for column in columns_to_anonymize:
        if column in dataframe.columns:
            dataframe[column] = dataframe[column].apply(lambda x: anonymize_value(x, salt))

    # получаем связанные данные по ID
    for index, row in dataframe.iterrows():
        esia_data = fetch_data_by_id(api_url, row['esia_id'], 'buyers')  # данные о покупателе по esia_id
        if esia_data:
            dataframe.at[index, 'buyer_data'] = str(esia_data)  # добавляем данные о покупателе в новый столбец
        
        event_data = fetch_data_by_id(api_url, row['event_id'], 'events')  # данные о событии по event_id
        if event_data:
            dataframe.at[index, 'event_data'] = str(event_data)  # добавляем данные о событии в новый столбец
        
        rrn_data = fetch_data_by_id(api_url, row['RRN'], 'transactions')  # данные о транзакции по RRN
        if rrn_data:
            dataframe.at[index, 'transaction_data'] = str(rrn_data)  # добавляем данные о транзакции в новый столбец
        
        ticket_data = fetch_data_by_id(api_url, row['ticket_id'], 'tickets')  # данные о билетах по ticket_id
        if ticket_data:
            dataframe.at[index, 'ticket_data'] = str(ticket_data)  # добавляем данные о билетах в новый столбец
    
    return dataframe

# пример пользования
if __name__ == "__main__":
    input_path = 'input_data.csv'  # путь к входному файлу с данными
    output_path = 'anonymized_data.json'  # путь к файлу для сохранения обезличенных данных
    columns = ['first_name', 'last_name', 'address', 'phone_number', 'email']  # кколонки для обезличивания
    salt = 'random_salt_string'  # соль
    user_id_column = 'esia_id'  # колонка с уникальными идентификаторами пользователей
    api_url = 'https://api.clovery.com'  # URL для запроса данных по айди

    # загрузка исходных данных
    data = load_data(input_path)

    # обезличивание данных и сбор связанных данных
    anonymized_data = anonymize_and_fetch_data(data, columns, salt, user_id_column, api_url)

    # сохранение обезличенных данных
    save_data(anonymized_data, output_path)

    print(f"Данные успешно обезличены и сохранены в {output_path}")