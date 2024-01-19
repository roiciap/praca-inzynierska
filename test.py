import psycopg2
from psycopg2 import sql

db_params = {
    'host': 'localhost',  # 'postgres',
    'database': 'database',
    'user': 'mateuszb',
    'password': 'mbazior',
    'port': 5432
}

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

analysist_query = """ 
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
    sg.name,
    pg.name
    
FROM
    learning_analysis.song_genre_for_model lrg
    JOIN learning_analysis.song s ON s.id = lrg.song_id
    JOIN learning_analysis.genre sg ON sg.id = s.genre_id
    JOIN learning_analysis.genre pg ON pg.id = lrg.genre_id
    JOIN learning_analysis.learn_results m ON m.id = lrg.model_id
    JOIN
    MaxPredictions mp ON lrg.song_id = mp.song_id AND lrg.model_id = mp.model_id AND lrg.prediction = mp.max_prediction
    WHERE sg.name != pg.name AND m.id = 95
    GROUP BY sg.name, pg.name
    ORDER BY ilosc DESC;"""
sql_query = sql.SQL(analysist_query)
cursor.execute(sql_query)
records = cursor.fetchall()
for i in records:
    print(i)
print(len(records))
# sql_query = sql.SQL(
#     """SELECT SUM(EXTRACT(SECOND FROM (time_end - time_start))) AS sum_of_time_diff
# FROM learning_analysis.learn_results;""")
# cursor.execute(sql_query)
# records = cursor.fetchall()
# print(records)


cursor.close()
conn.close()
