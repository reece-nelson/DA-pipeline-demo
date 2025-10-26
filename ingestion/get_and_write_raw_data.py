import requests
import pandas as pd
import psycopg2
import json

def get_data():
    API_KEY = 'WN8wg69p6YVSN0bw92BUC179qYx5PKCfLvVQGxCM'
    BASE_URL = 'https://api.eia.gov/v2/electricity/retail-sales/data/'
    PARAMS = {
        'frequency': 'monthly',
        'data[0]': 'customers',
        'data[1]': 'price',
        'data[2]': 'revenue',
        'data[3]': 'sales',
        'start': '2001-01',
        'end': '2025-07',
        'offset': 0,
        'api_key': API_KEY
    }
    all_data = []
    batch_size = 5000
    done = False

    while not done:
        print(f"Fetching records starting at offset {PARAMS['offset']}...")
        response = requests.get(BASE_URL, params=PARAMS)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        json_data = response.json()
        records = json_data.get('response', {}).get('data', [])
        all_data.extend(records)

        if len(records) < batch_size:
            done = True
        else:
            PARAMS['offset'] += batch_size
    return all_data

def write_eia_to_postgresql(api_data):
    df = pd.DataFrame(api_data)

    # write this to bronze layer
    conn = psycopg2.connect(
        dbname="default_database",
        user="username",
        password="password",
        port="5432",
        host="postgresdb"
    )   
    cur = conn.cursor()

    df.columns = [col.replace('-', '') for col in df.columns]
    columns = ', '.join(df.columns)
    values = ', '.join(['%s'] * len(df.columns))
    
    insert_query = f"INSERT INTO bronze.raw_eia ({columns}) VALUES ({values})"
    data = list(df.itertuples(index=False, name=None))
    cur.executemany(insert_query, data)
    conn.commit()
    cur.close()
    conn.close()


def write_nhl_to_postgresql(data):
    # write this to bronze layer
    conn = psycopg2.connect(
        dbname="default_database",
        user="username",
        password="password",
        port="5432",
        host="postgresdb"
    )   
    cur = conn.cursor()

    data = json.loads(data)
    columns = data[0].keys()
    columns_str = ", ".join(columns)
    values = ", ".join([f"%({col})s" for col in columns])
    
    insert_query = f"INSERT INTO bronze.raw_nhl_us_teams ({columns_str}) VALUES ({values})"
    cur.executemany(insert_query, data)
    conn.commit()
    cur.close()
    conn.close()


    