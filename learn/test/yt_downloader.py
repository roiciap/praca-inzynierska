import os
from concurrent.futures.thread import ThreadPoolExecutor

from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube

from consts import GENRES_SORTED

songs = {
    'blues': [

    ],
    'classical': [

    ],
    'country': [

    ],
    'disco': [

    ],
    'hiphop': [

    ],
    'jazz': [

    ],
    'metal': [

    ],
    'pop': [

    ],
    'reggae': [

    ],
    'rock': [

    ],
}


def download_song(yt_url, genre):
    yt = YouTube(yt_url)
    video = yt.streams.filter(only_audio=True).get_audio_only()
    destination = './tmp/{}'.format(genre)
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    mp4_filename = "{}{}".format(base, ext)
    mp3_filename = "{}.mp3".format(base, ext)
    audio = AudioFileClip(mp4_filename)
    audio.write_audiofile(mp3_filename)
    os.remove(mp4_filename)


def download_for_genre(genre):
    genre_songs = songs[genre]
    with ThreadPoolExecutor() as executor:
        # Uruchom funkcję process_song dla każdego utworu w osobnym wątku
        futures = [executor.submit(download_song, yt_song, genre) for yt_song in genre_songs]
        for i in futures:
            i.result()


for genre in GENRES_SORTED:
    download_for_genre(genre)
