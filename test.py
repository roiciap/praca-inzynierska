import numpy
import requests

from run.domain.prediction_domain import load_mfcc

filenames = [
    './run/app/tmp/95BPM.mp3',
    './run/app/tmp/Nirvana - Rape Me [Lyrics].mp3',
    './run/app/tmp/Queen - Under Pressure (Official Video).mp3',
    './run/app/tmp/Led Zeppelin - Stairway To Heaven (Official Audio).mp3',
    './run/app/tmp/Queen  Bohemian Rhapsody (Official Video Remastered).mp3',
]

files = [
    {'file': open(file_name, 'rb')} for file_name in filenames
]
# responses = [requests.get('http://127.0.0.1:5000/predict', files=f) for f in files]
# for r in responses:
#     print(r.json())


import librosa

from shared.mfcc_creator import load_song_wav, add_tempo_to_mfcc

for f in filenames:
    signal, sr = load_song_wav(f)
    tempo, _ = librosa.beat.beat_track(y=signal, sr=sr)

    print(f, tempo)
    mfccs = load_mfcc(f)
    tiempi = numpy.full((mfccs.shape[0]), tempo)
    print(mfccs.shape)
    mix = add_tempo_to_mfcc(mfccs, tiempi)
    print(mix.shape)

