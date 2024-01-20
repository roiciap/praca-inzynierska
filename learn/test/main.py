import os

import psycopg2
from keras.saving.save import load_model
from psycopg2 import sql

from consts import GENRES_SORTED
from learn.test.test_consts import WITH_DATA_DROP, model_ids_to_run
from learn.test.test_model import test_song
from run.domain.prediction_domain import load_mfcc, predict_labels

songs_path = "tmp"
models_path = "../databases/volumes/models"

db_params = {
    'host': 'localhost',  # 'postgres',
    'database': 'database',
    'user': 'mateuszb',
    'password': 'mbazior',
    'port': 5432
}


def get_all_songs():
    songs = {}
    for genre in GENRES_SORTED:
        songs[genre] = []
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(songs_path)):
        # bo pierwsza iteracja to folder główny
        if dirpath is not songs_path:
            dirpath_components = dirpath.split("\\")
            semantic_label = dirpath_components[-1]
            genre = semantic_label
            for f in filenames:
                songs[genre].append(f)
    return songs


def data_drop():
    if not WITH_DATA_DROP:
        return
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    # usunięcie danych tabel
    tables_to_drop = [
        "learning_analysis.song_genre_for_model",
        "learning_analysis.song",
        "learning_analysis.genre",
    ]
    drop_queries = ["DELETE FROM {}".format(table) for table in tables_to_drop]
    for query in drop_queries:
        sql_query = sql.SQL(query)
        cursor.execute(sql_query)
    conn.commit()
    # dodanie wszystkich gatunków
    for i in GENRES_SORTED:
        sql_query = sql.SQL("INSERT INTO learning_analysis.genre (name) VALUES ('{}')".format(i))
        cursor.execute(sql_query)
    conn.commit()
    songs = get_all_songs()
    for genre in GENRES_SORTED:
        genre_songs = songs[genre]
        for song in genre_songs:
            query = """INSERT INTO learning_analysis.song (name, genre_id)
VALUES (
    '{}',
    (SELECT id FROM learning_analysis.genre WHERE name = '{}')
);
""".format(song, genre)
            sql_query = sql.SQL(query)
            cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()


def read_songs():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    sql_query = sql.SQL("SELECT s.id, s.name, s.genre_id, g.name FROM learning_analysis.song s" +
                        " JOIN learning_analysis.genre g ON g.id = s.genre_id")
    cursor.execute(sql_query)
    records = cursor.fetchall()

    return_data = [test_song(song[0], song[1], song[2], song[3]) for song in records]

    cursor.close()
    conn.close()
    return return_data


def load_songs(songs):
    for song in songs:
        song_path = os.path.join(songs_path, song.genre_name, song.name)
        print("odczytuje piosenke: " + song_path)
        mfccs = load_mfcc(song_path)
        song.set_mfcc(mfccs)
    return songs


def predict_single_song(model, song):
    label_averages = predict_labels(model, song.mfcc)
    return label_averages  # [label, value]


def write_prediciton_response(model_id, song_id, predictions):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    for genre in GENRES_SORTED:

        query = """INSERT INTO learning_analysis.song_genre_for_model (model_id, song_id, genre_id, prediction)
VALUES (
    {},
    {},
    (SELECT id FROM learning_analysis.genre WHERE name = '{}'),
    {}
);
""".format(model_id, song_id, genre, predictions[genre])
        sql_query = sql.SQL(query)
        cursor.execute(sql_query)
    conn.commit()
    cursor.close()
    conn.close()


def make_predictions(songs):
    for model_id in model_ids_to_run:
        model_path = os.path.join(models_path, "{}.h5".format(model_id))
        print("odczytuje model: " + model_path)
        model = load_model(model_path)
        for song in songs:
            predicitions = predict_single_song(model, song)
            write_prediciton_response(model_id, song.id, predicitions)


if __name__ == '__main__':
    data_drop()
    songs = read_songs()
    songs_data = load_songs(songs)
    make_predictions(songs_data)
