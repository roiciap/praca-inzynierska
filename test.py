from concurrent.futures.thread import ThreadPoolExecutor

import requests
from moviepy.editor import *
from pytube import YouTube

yt_songs = [
    {'genre': 'hiphop', 'url': 'https://www.youtube.com/watch?v=MPWrsPp0M8k'},
    {'genre': 'blues', 'url': 'https://www.youtube.com/watch?v=RR8-m7AtzvM'},
    {'genre': 'jazz', 'url': 'https://www.youtube.com/watch?v=GohBkHaHap8'},
    {'genre': 'metal', 'url': 'https://www.youtube.com/watch?v=E0ozmU9cJDg'},
    {'genre': 'disco', 'url': 'https://www.youtube.com/watch?v=CS9OO0S5w2k'},
    {'genre': 'rock', 'url': 'https://www.youtube.com/watch?v=RbmS3tQJ7Os'},
    {'genre': 'reggae', 'url': 'https://www.youtube.com/watch?v=-JhwxTen6yA'},
    {'genre': 'classical', 'url': 'https://www.youtube.com/watch?v=9E6b3swbnWg'},
    {'genre': 'country', 'url': 'https://www.youtube.com/watch?v=mUFObCZtGWQ'},
    {'genre': 'pop', 'url': 'https://www.youtube.com/watch?v=fWNaR-rxAic'},
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
    # files_req = {'file': open(mp3_filename, 'rb')}
    # response = requests.post('http://127.0.0.1:5000/predict', files=files_req)
    # print(genre_dir, response.json())


with ThreadPoolExecutor() as executor:
    # Uruchom funkcję process_song dla każdego utworu w osobnym wątku
    futures = [executor.submit(download_song_and_check, yt_song) for yt_song in yt_songs]
    for i in futures:
        i.result()

