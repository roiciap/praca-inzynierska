from datetime import datetime

import redis
import json

import psycopg2
from psycopg2 import sql

# Zdefiniuj dane do połączenia z bazą danych
db_params = {
    'host': 'localhost',
    'database': 'database',
    'user': 'mateuszb',
    'password': 'mbazior',
    'port': 5432
}

# Utwórz połączenie z bazą danych



with redis.Redis() as Client:
    while True:
        result_json = Client.brpop('results')[1]
        result = json.loads(result_json)
        # Utwórz kursor do wykonywania poleceń SQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Przykładowe dane do wstawienia
        data_to_insert = {
            **result,
            'time_start': datetime.fromtimestamp(result['time_start']),
            'time_end': datetime.fromtimestamp(result['time_end'])
        }
        print(data_to_insert)

        # Utwórz polecenie SQL do wstawienia danych
        insert_query = sql.SQL("INSERT INTO learning_analysis.learn_results ({}) VALUES ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, data_to_insert.keys())),
            sql.SQL(', ').join(map(sql.Literal, data_to_insert.values()))
        )

        # Wykonaj operację insert
        cursor.execute(insert_query, data_to_insert)
        # Zatwierdź zmiany
        conn.commit()

        # Zamknij kursor i połączenie
        cursor.close()
        conn.close()
