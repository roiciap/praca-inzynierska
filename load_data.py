import json
import math
import os
import librosa

DATASET_PATH = "input_data"
JSON_PATH = "data.json"
SAMPLE_RATE = 22050
SEGMENT_DURATION=3

def create_json(dataset_path, json_path, n_mfcc=13, n_fft=2048, hop_length=512):  # , num_segments=5):
    data = {
        "mapping": [],
        "mfcc": [],
        "tempo": [],
        "labels": []
    }
    # zaokrąglenie w górę
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
        # bo pierwsza iteracja to folder główny
        if dirpath is not dataset_path:
            dirpath_components = dirpath.split("\\")
            semantic_label = dirpath_components[-1]
            data["mapping"].append(semantic_label)

            for f in filenames:
                # todo tutaj moze nie będzie trzeba zaczytywać całego pliku 2 razy

                # zaczytanie dlugosci utworu a następnie zaczytanie utworu,
                # ale jedynie długości podzielnej przez długość segmentu tak aby nie zostawał na końcu 'niepełny' segment
                file_path = os.path.join(dirpath, f)
                signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)
                duration = librosa.get_duration(y=signal, sr=sr)
                duration_to_re_read = math.floor(duration/SEGMENT_DURATION) * SEGMENT_DURATION

                signal, sr = librosa.load(file_path, sr=SAMPLE_RATE, duration=duration_to_re_read)
                duration = librosa.get_duration(y=signal, sr=sr)
                SAMPLES_PER_TRACK = sr * duration
                # dzielimy utwory na segmenty 3 sekundowe
                num_segments = int(duration / SEGMENT_DURATION)

                num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)

                expected_mffc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)

                # todo to do ustalenia czy wyciągać tempo fragmentów czy całej piosenki
                # tempo, beat_frames = librosa.beat.beat_track(y=signal, sr=sr)
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
                        data["mfcc"].append(mfcc.tolist())
                        # data["tempo"].append(tempo)
                        data["labels"].append(i - 1)
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)


create_json(DATASET_PATH, JSON_PATH)  # , num_segments=10)

