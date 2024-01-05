import math

import librosa


def load_song_wav(file_path,segment_duration, sample_rate ):
    signal, sr = librosa.load(file_path, sr=sample_rate)
    duration = librosa.get_duration(y=signal, sr=sr)
    duration_to_re_read = math.floor(duration / segment_duration) * segment_duration

    return librosa.load(file_path, sr=sample_rate, duration=duration_to_re_read)


def split_song_on_mfcc_segments(signal, sr, segment_duration, n_mfcc=13, n_fft=2048, hop_length=512):
    output = []
    duration = librosa.get_duration(y=signal, sr=sr)
    SAMPLES_PER_TRACK = sr * duration
    # dzielimy utwory na segmenty 3 sekundowe
    num_segments = int(duration / segment_duration)

    num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)

    expected_mffc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)
    for s in range(num_segments):
        start_sample = num_samples_per_segment * s
        finish_sample = start_sample + num_samples_per_segment

        mfcc = librosa.feature.mfcc(
            y=signal[start_sample:finish_sample],
            sr=sr,
            n_fft=n_fft,
            n_mfcc=n_mfcc,
            hop_length=hop_length
        )
        # łatwiej się tak pracuje
        mfcc = mfcc.T
        if len(mfcc) == expected_mffc_vectors_per_segment:
            output.append(mfcc.tolist())
    return output
