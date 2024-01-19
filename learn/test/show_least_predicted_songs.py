import os
import shutil

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
    s.name
FROM
    learning_analysis.song_genre_for_model lrg
    JOIN learning_analysis.song s ON s.id = lrg.song_id
    JOIN learning_analysis.genre sg ON sg.id = s.genre_id
    JOIN learning_analysis.genre pg ON pg.id = lrg.genre_id
    JOIN learning_analysis.learn_results m ON m.id = lrg.model_id
    JOIN
    MaxPredictions mp ON lrg.song_id = mp.song_id AND lrg.model_id = mp.model_id AND lrg.prediction = mp.max_prediction
    WHERE sg.name != pg.name AND time_start > '{}' 
    GROUP BY s.name, sg.name
    ORDER BY ilosc DESC;
""".format(MODELS_TRAINED_SINCE)
sql_query = sql.SQL(analysist_query)
cursor.execute(sql_query)
records = cursor.fetchall()

for i in records:
    print("ilość błędnych: {}, gatunek: {}, nazwa: {}".format(i[0], i[1], i[2]))
    # shutil.move(os.path.join('tmp', i[1], i[2]), os.path.join('../../input_data', i[1], i[2]))


cursor.close()
conn.close()
