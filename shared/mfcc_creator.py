import math

import librosa
import numpy as np

from consts import SEGMENT_DURATION, SAMPLE_RATE, WITH_TEMPO, THRESHOLD_ENERGY, REMOVE_SILENT


def load_song_wav(file_path, segment_duration=SEGMENT_DURATION, sample_rate=SAMPLE_RATE):
    signal, sr = librosa.load(file_path, sr=sample_rate)
    duration = librosa.get_duration(y=signal, sr=sr)
    duration_to_re_read = math.floor(duration / segment_duration) * segment_duration

    return librosa.load(file_path, sr=sample_rate, duration=duration_to_re_read)



def split_song_on_mfcc_segments(signal, sr=SAMPLE_RATE, segment_duration=SEGMENT_DURATION, n_mfcc=13, n_fft=2048,
                                hop_length=512, remove_silent=REMOVE_SILENT):
    mfccs = []
    skipped_indexes = []
    duration = librosa.get_duration(y=signal, sr=sr)
    num_segments = int(duration / segment_duration)

    num_samples_per_segment = sr * segment_duration
    expected_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)
    for s in range(num_segments):
        start_sample = num_samples_per_segment * s
        finish_sample = start_sample + num_samples_per_segment
        segment_signal = signal[start_sample:finish_sample]
        # if average of segment energy is bellow const THRESHOLD_ENERGY its skipped
        if remove_silent and np.mean(abs(segment_signal)) < THRESHOLD_ENERGY:
            skipped_indexes.append(s)
            continue

        mfcc = librosa.feature.mfcc(
            y=segment_signal,
            sr=sr,
            n_fft=n_fft,
            n_mfcc=n_mfcc,
            hop_length=hop_length
        )
        mfcc = mfcc.T

        if len(mfcc) == expected_mfcc_vectors_per_segment:
            mfccs.append(mfcc.tolist())
    return mfccs, skipped_indexes


def add_tempo_to_mfcc(mfcc, tempo):
    if isinstance(mfcc, list):
        X_mfcc = np.array(mfcc)
    if isinstance(mfcc, np.ndarray):
        X_mfcc = mfcc
    if not WITH_TEMPO:
        return X_mfcc
    else:
        if isinstance(tempo, float):
            # robie array tempa w takim samym kształcie jak mfcc poza ostatnim wymiarem - tam 1
            tempo_array = np.full_like(X_mfcc[..., :1], tempo)
        elif isinstance(tempo, np.ndarray) and tempo.shape == (X_mfcc.shape[0],):
            tempo_shape = X_mfcc[..., :1].shape
            tempo_array = np.zeros(tempo_shape, dtype=float)

            # Wypełnianie tablicy zgodnie z warunkami
            for i in range(0, tempo_shape[0]):
                for j in range(0, tempo_shape[1]):
                    tempo_array[i, j, 0] = tempo[i]

        X_combined = np.concatenate((X_mfcc, tempo_array), axis=-1)
        return X_combined
