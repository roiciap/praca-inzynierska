import json
import os

from consts import SEGMENT_DURATION, SAMPLE_RATE
from shared.mfcc_creator import split_song_on_mfcc_segments, load_song_wav



def calculate_data_file(dataset_path, n_mfcc=13, n_fft=2048, hop_length=512):  # , num_segments=5):
    data = {
        "mapping": [],
        "mfcc": [],
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
                print(f)
                file_path = os.path.join(dirpath, f)
                signal, sr = load_song_wav(file_path, SEGMENT_DURATION, sample_rate=SAMPLE_RATE)
                song_segments = split_song_on_mfcc_segments(signal, sr, SEGMENT_DURATION,
                                                            n_mfcc=n_mfcc,
                                                            n_fft=n_fft,
                                                            hop_length=hop_length)
                for segment in song_segments:
                    data["mfcc"].append(segment)
                    data["labels"].append(i - 1)
    return data


with open('data.json', "w") as fp:
    json.dump(calculate_data_file('input_data'), fp, indent=4)
