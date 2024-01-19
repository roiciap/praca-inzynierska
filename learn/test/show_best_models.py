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
    """SELECT *
      FROM learning_analysis.learn_results
       WHERE time_start > '{}'
       ORDER BY {} DESC LIMIT 3""".format(
        MODELS_TRAINED_SINCE, sort) for sort in sort_by]

for query in queries:
    sql_query = sql.SQL(query)
    cursor.execute(sql_query)
    records = cursor.fetchall()
    print(records)

analysis =""" 
WITH MaxPredictions AS (
    SELECT
        lrg.song_id,
        lrg.model_id,
        MAX(lrg.prediction) AS max_prediction
    FROM
        learning_analysis.song_genre_for_model lrg
    GROUP BY
        lrg.song_id, lrg.model_id
)

SELECT
    count(*) as ilosc,
    m.id
FROM
    learning_analysis.song_genre_for_model lrg
    JOIN learning_analysis.song s ON s.id = lrg.song_id
    JOIN learning_analysis.genre sg ON sg.id = s.genre_id
    JOIN learning_analysis.genre pg ON pg.id = lrg.genre_id
    JOIN learning_analysis.learn_results m ON m.id = lrg.model_id
    JOIN
    MaxPredictions mp ON lrg.song_id = mp.song_id AND lrg.model_id = mp.model_id AND lrg.prediction = mp.max_prediction
    WHERE sg.name != pg.name
    GROUP BY m.id
    ORDER BY ilosc DESC;""".format(MODELS_TRAINED_SINCE)
sql_query = sql.SQL(analysis)
cursor.execute(sql_query)
records = cursor.fetchall()
for i in records:
    print("zlych: {}, model: {}".format(i[0], i[1]))

sql_query = sql.SQL("Select * from learning_analysis.learn_results where id=95")
cursor.execute(sql_query)
records = cursor.fetchall()
print(records[0])

cursor.close()
conn.close()
