from concurrent.futures.thread import ThreadPoolExecutor

import requests
from moviepy.editor import *
from pytube import YouTube

yt_songs = [
    {'genre': 'hiphop', 'url': 'https://www.youtube.com/watch?v=k_aXaK0GSEk'},
]

def download_song_and_check(yt_song):
    genre_dir = yt_song['genre']
    yt_url = yt_song['url']
    yt = YouTube(yt_url)
    video = yt.streams.filter(only_audio=True).get_audio_only()
    destination = './tmp/{}'.format(genre_dir)
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    mp4_filename = "{}{}".format(base, ext)
    mp3_filename = "{}.mp3".format(base, ext)
    audio = AudioFileClip(mp4_filename)
    audio.write_audiofile(mp3_filename)
    os.remove(mp4_filename)
    files_req = {'file': open(mp3_filename, 'rb')}
    response = requests.get('http://127.0.0.1:5000/predict', files=files_req)
    print(genre_dir, response.json())


with ThreadPoolExecutor() as executor:
    # Uruchom funkcję process_song dla każdego utworu w osobnym wątku
    futures = [executor.submit(download_song_and_check, yt_song) for yt_song in yt_songs]
    for i in futures:
        i.result()

