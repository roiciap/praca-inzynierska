import numpy
from keras.saving.save import load_model

from consts import SEGMENT_DURATION, SAMPLE_RATE, GENRES_SORTED
from shared.mfcc_creator import load_song_wav, split_song_on_mfcc_segments

signal, sr = load_song_wav('./tmp/kukon-mini.wav', SEGMENT_DURATION, SAMPLE_RATE)
# signal, sr = load_song_wav('./tmp/kukon-mini-beat.wav', SEGMENT_DURATION, SAMPLE_RATE)
# signal, sr = load_song_wav('./tmp/jakis-rap.wav', SEGMENT_DURATION, SAMPLE_RATE)
# signal, sr = load_song_wav('./tmp/rock.00000.wav', SEGMENT_DURATION, SAMPLE_RATE)
mfccs = split_song_on_mfcc_segments(signal, sr, SEGMENT_DURATION)

# wszystkie
mfcc = numpy.array(mfccs)

# pierwsze
# mfcc = numpy.array(mfccs[0])
# mfcc = numpy.expand_dims(mfcc, axis=0)
# predykcja
model = load_model('./tmp/model.h5')
predictions = model.predict(mfcc)
print(len(predictions))

# wyliczenie sredniej dla kazdego labela
label_averages = numpy.zeros(10)
for sample_prediction in predictions:
    for prediction in range(len(sample_prediction)):
        label_averages[prediction] += sample_prediction[prediction]

for i in range(len(label_averages)):
    label_averages[i] = label_averages[i] / len(predictions)

# posortowanie po wartości labeli
output = []

for label in range(len(label_averages)):
    output.append({'label': GENRES_SORTED[label], 'value': label_averages[label]})

sorted_output = sorted(output, key=lambda x: x['value'], reverse=True)

print(sorted_output)
