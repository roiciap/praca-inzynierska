import os
from datetime import datetime
import random
from threading import Lock

from flask import Flask, request, jsonify
from keras.saving.save import load_model

from run.domain.prediction_domain import load_mfcc, get_sorted_outcome_with_labels, predict_labels

app = Flask(__name__)
prediction_lock = Lock()
MODEL = load_model('./model.h5')


def make_prediction(file_name):
    mfccs = load_mfcc(file_name)
    label_averages = predict_labels(MODEL, mfccs)

    return get_sorted_outcome_with_labels(label_averages)


@app.route('/predict', methods=['GET'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename.endswith('.mp3') or file.filename.endswith('.wav'):
            # wymyślenie nazwy pliku tak żeby wyeliminować szansę że zostaną przesłane 2 takie same
            timestamp = datetime.now().strftime("%M%S%f")[:-3]
            file_name = '{}-{}-{}'.format(timestamp, random.randint(1, 10000), file.filename)
            file_dir = './tmp/{}'.format(file_name)
            # zapis na chwilę pliku -> wykonanie predykcji -> usunięcie pliku
            file.save(file_dir)
            prediction_result = make_prediction(file_dir)
            os.remove(file_dir)
        return jsonify({
            'success': True,
            'result': prediction_result
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
