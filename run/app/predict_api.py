import os
from datetime import datetime
import random
from threading import Lock

import numpy
from flask import Flask, request, jsonify
from keras.saving.save import load_model

from consts import MODEL_TEST_NAME
from run.domain.prediction_domain import load_mfcc, predict_labels
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

prediction_lock = Lock()
MODEL = load_model('./{}'.format(MODEL_TEST_NAME))


def make_prediction(file_name):
    mfccs, skipped_indexes = load_mfcc(file_name)
    label_averages, all_predictions = predict_labels(MODEL, mfccs)

    return label_averages, all_predictions, skipped_indexes

def convert_to_builtin_type(obj):
    if isinstance(obj, numpy.float32):
        return float(obj)
    raise TypeError("Type not serializable")

@app.route('/predict', methods=['POST'])
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
            label_averages, all_predictions, skipped_indexes = make_prediction(file_dir)
            os.remove(file_dir)

        return jsonify({
            'success': True,
            'result': {
                "label_averages": label_averages,
                "all_predictions": all_predictions,
                "skipped_indexes": skipped_indexes
                       }
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
