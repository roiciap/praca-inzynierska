import psycopg2
from psycopg2 import sql

from learn.test.test_consts import MODELS_TRAINED_SINCE

db_params = {
    'host': 'localhost',  # 'postgres',
    'database': 'database',
    'user': 'mateuszb',
    'password': 'mbazior',
    'port': 5432
}



conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

sort_by = [
    "train_acc", "validation_acc", "test_acc"
]

queries = [
    """SELECT id,train_acc,validation_acc,test_acc
      FROM learning_analysis.learn_results
       WHERE time_start > '{}'
       ORDER BY {} DESC LIMIT 3""".format(
        MODELS_TRAINED_SINCE, sort) for sort in sort_by]

for query in queries:
    sql_query = sql.SQL(query)
    cursor.execute(sql_query)
    records = cursor.fetchall()
    print(records)

cursor.close()
conn.close()
