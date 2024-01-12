from datetime import datetime

import psycopg2
from flask import Flask, request, jsonify

from psycopg2 import sql

app = Flask(__name__)


db_params = {
    'host': 'postgres',
    'database': 'database',
    'user': 'mateuszb',
    'password': 'mbazior',
    'port': 5432
}


def save_to_db(
        epochs,
        batch_size,
        learning_rate,
        lstm_1,
        lstm_2,
        dense,
        dropout,
        test_acc,
        train_acc,
        validation_acc,
        time_start,
        time_end,
        worker,
        segment_duration,
        with_tempo
):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    data_to_insert = {
        'epochs': epochs,
        'batch_size': batch_size,
        'learning_rate': learning_rate,
        'lstm_1': lstm_1,
        'lstm_2': lstm_2,
        'dense': dense,
        'dropout': dropout,
        'test_acc': test_acc,
        'train_acc': train_acc,
        'validation_acc': validation_acc,
        'time_start': time_start,
        'time_end': time_end,
        'time_start': datetime.fromtimestamp(time_start),
        'time_end': datetime.fromtimestamp(time_end),
        'worker':worker,
        'segment_duration': segment_duration,
        'with_tempo': with_tempo
    }
    print('insertuje', data_to_insert)

    # Utwórz polecenie SQL do wstawienia danych
    insert_query = sql.SQL("INSERT INTO learning_analysis.learn_results ({}) VALUES ({}) RETURNING id").format(
        sql.SQL(', ').join(map(sql.Identifier, data_to_insert.keys())),
        sql.SQL(', ').join(map(sql.Literal, data_to_insert.values()))
    )

    # Wykonaj operację insert
    cursor.execute(insert_query, data_to_insert)
    # Zatwierdź zmiany
    conn.commit()

    model_id = cursor.fetchone()[0]

    # Zamknij kursor i połączenie
    cursor.close()
    conn.close()
    return model_id


@app.route('/upload_model', methods=['POST'])
def upload_model():
    try:
        # Sprawdź, czy przesłano plik
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        # Sprawdź, czy plik ma odpowiednie rozszerzenie
        if file.filename.endswith('.h5'):
            # Zapisz plik na serwerze
            model_id = save_to_db(epochs=int(request.args.get('epochs')),
                                  batch_size=int(request.args.get('batch_size')),
                                  learning_rate=float(request.args.get('learning_rate')),
                                  lstm_1=int(request.args.get('lstm_1')),
                                  lstm_2=int(request.args.get('lstm_2')),
                                  dense=int(request.args.get('dense')),
                                  dropout=float(request.args.get('dropout')),
                                  test_acc=float(request.args.get('test_acc')),
                                  train_acc=float(request.args.get('train_acc')),
                                  validation_acc=float(request.args.get('validation_acc')),
                                  time_start=float(request.args.get('time_start')),
                                  time_end=float(request.args.get('time_end')),
                                  worker=request.args.get('worker'),
                                  with_tempo=request.args.get('with_tempo'),
                                  segment_duration=int(request.args.get('segment_duration'))
                                  )
            file.save('./models/{}.h5'.format(model_id))

            return jsonify({
                'success': 'Model uploaded and loaded successfully'
            }), 200
        else:
            return jsonify({'error': 'Invalid file format. Expected .h5'}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/')
def xd():
    return "witaj hindusie"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
