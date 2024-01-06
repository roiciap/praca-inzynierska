import librosa
import numpy

from consts import SEGMENT_DURATION, SAMPLE_RATE, GENRES_SORTED
from shared.mfcc_creator import load_song_wav, split_song_on_mfcc_segments, add_tempo_to_mfcc


def load_mfcc(file_name):
    signal, sr = load_song_wav(file_name, SEGMENT_DURATION, SAMPLE_RATE)
    mfccs = split_song_on_mfcc_segments(signal, sr, SEGMENT_DURATION)
    tempo, _ = librosa.beat.beat_track(y=signal, sr=sr)
    return add_tempo_to_mfcc(mfccs, tempo)


def predict_labels(model, mfcc):
    predictions = model.predict(mfcc)

    # wyliczenie sredniej dla kazdego labela
    label_averages = numpy.zeros(10)
    for sample_prediction in predictions:
        for prediction in range(len(sample_prediction)):
            label_averages[prediction] += sample_prediction[prediction]
    for i in range(len(label_averages)):
        label_averages[i] = label_averages[i] / len(predictions)
    return label_averages


def get_sorted_outcome_with_labels(label_averages):
    # posortowanie po wartości labeli
    output = []

    for label in range(len(label_averages)):
        output.append({'label': GENRES_SORTED[label], 'value': label_averages[label]})

    return sorted(output, key=lambda x: x['value'], reverse=True)
