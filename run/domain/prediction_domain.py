import librosa
import numpy

from consts import SEGMENT_DURATION, SAMPLE_RATE, GENRES_SORTED
from shared.mfcc_creator import load_song_wav, split_song_on_mfcc_segments, add_tempo_to_mfcc


def load_mfcc(file_name):
    signal, sr = load_song_wav(file_name, SEGMENT_DURATION, SAMPLE_RATE)
    mfccs, skipped_indexes = split_song_on_mfcc_segments(signal, sr, SEGMENT_DURATION)
    tempo, _ = librosa.beat.beat_track(y=signal, sr=sr)
    mfccs = add_tempo_to_mfcc(mfccs, tempo)
    return mfccs, skipped_indexes


def predict_labels(model, mfcc):
    predictions = model.predict(mfcc)

    # wyliczenie sredniej dla kazdego labela
    label_averages = dict()
    for genre in GENRES_SORTED:
        label_averages[genre] = 0
    all_predictions = []
    for sample_prediction in predictions:
        this_predictions = dict()
        for prediction in range(len(sample_prediction)):
            if sample_prediction[prediction] < 0.0001:
                this_predictions[GENRES_SORTED[prediction]] = 0
            else:
                this_predictions[GENRES_SORTED[prediction]] = float(sample_prediction[prediction])
        all_predictions.append(this_predictions)
    for prediction in all_predictions:
        for genre in GENRES_SORTED:
            label_averages[genre] += prediction[genre]
    for genre in GENRES_SORTED:
        label_averages[genre] = label_averages[genre] / len(predictions)
    return label_averages, all_predictions


