import librosa, librosa.display, librosa.feature
import matplotlib.pyplot as plt
import numpy as np
def process_file(file):
    # load .wav file
    signal,sr = librosa.load(file, sr=22050)
    # TMP wyświetl waveform
    # librosa.display.waveplot(signal, sr=sr)
    # plt.xlabel("Time")
    # plt.ylabel("Amplitude")
    # plt.show()
    ######
    # fft -> spectrum
    fft = np.fft.fft(signal)
    magnitude = np.abs(fft)
    frequency = np.linspace(0, sr, len(magnitude))
    #podzielenie frequency i magnitude ponieważ prawa połowa wykresu spectrum jest lustrzanym odbiciem lewej
    left_frequency = frequency[:int(len(frequency)/2)]
    left_magnitude = magnitude[:int(len(frequency)/2)]
    # TMP wyświetl spectrum
    # plt.plot(left_frequency, left_magnitude)
    # plt.xlabel("Frequency")
    # plt.ylabel("Magnitude")
    # plt.show()
    ######
    # stft -> spectogram
    n_fft = 2048
    hop_length = 512
    stft = librosa.core.stft(signal, hop_length=hop_length, n_fft=n_fft)
    spectogram = np.abs(stft)

    log_spectogram = librosa.amplitude_to_db(spectogram)

    # TMP wyświetl spectogram
    # librosa.display.specshow(log_spectogram, sr=sr, hop_length=hop_length)
    # plt.xlabel("Time")
    # plt.ylabel("Frequency")
    # plt.colorbar()
    # plt.show()
    #####
    # MFCCs
    MFFCs = librosa.feature.mfcc(y=signal, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)
    # TMP wyświetl MFFC
    librosa.display.specshow(MFFCs, sr=sr, hop_length=hop_length)
    plt.xlabel("Time")
    plt.ylabel("MFCC")
    plt.colorbar()
    plt.show()


process_file("input_data/rock/rock.00015.wav")