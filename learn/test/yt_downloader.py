import os
from concurrent.futures.thread import ThreadPoolExecutor

from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube

from consts import GENRES_SORTED

songs = {
    'blues': [
        'https://youtu.be/UiHmeHZAc0s?si=dUS7qj3Tbtsi6bZK',
        'https://youtu.be/S5NPriAa8so?si=xq_JpX9lsYziXPuY',
        'https://youtu.be/N-KluFB9A8M?si=-6a0B0tzYR_-JNfu',
        'https://youtu.be/MqBfAvScyds?si=9MLcQSgGCryIpytO',
        'https://youtu.be/uwt6edSnXk4?si=S_r-k60bnW732-SE'
    ],

    'classical': [
        'https://www.youtube.com/watch?v=rrVDATvUitA',
        'https://youtu.be/_FeJFs6LJjU?si=bXrEwX7oQxAJgvzE',
        'https://youtu.be/-HNmVe0Mmek?si=HjSflftK9Q95lxu6'
    ],

    'country': [
        'https://youtu.be/EQfm-Qqy-wU?si=4SxkFUItAV5K-2tc',
        'https://youtu.be/ZsEjZKNzt9E?si=ve6hwU2OsP3YSmC1',
        'https://youtu.be/UQtiiDrL_O4?si=g23Y5xvz7PfvZWTA',
        'https://youtu.be/rct9Zs_Yd-I?si=XxcC3GcL7AgxwOaW',
        'https://youtu.be/q4webhCu8bY?si=u7ocmLAZ9G43t29Z',
        'https://youtu.be/bN8vY8qkgVs?si=_nXfkHdjBeli6BaD',
        'https://youtu.be/p_IwENcMPOA?si=H4AP_C-oOZDtyiHn',
        'https://youtu.be/o1C3mVUkAt8?si=IQHOP55h7BjlLZ6J'
    ],

    'disco': [
        'https://youtu.be/I_izvAbhExY?si=Z1jieoLBUH4UD8I0',
        'https://youtu.be/q5uMOOQ6MV0?si=sxZyLbY5LlFt-xVw',
        'https://youtu.be/_EtKpw_LJZo?si=tiPV8tVSJYnhKe6C'
    ],

    'hiphop': [
        'https://youtu.be/Ldne1nTSdFM?si=8YLpGLLCjhsO6P9H',
        'https://youtu.be/-FZ0if9q1kU?si=krr14Wlp70H19sFs',
        'https://youtu.be/eJO5HU_7_1w?si=xtErr0cxV_DP_RAa',
        'https://youtu.be/5-Pyr_Xg91U?si=QV33e7JWg6Nl3vIZ',
        'https://youtu.be/l0U7SxXHkPY?si=-C3Ky-k9_BLZqWWg',
        'https://youtu.be/PEGccV-NOm8?si=G1QFvCunh10QPinw'
    ],

    'jazz': [
        'https://youtu.be/KLeMDhGs5W8?si=fvM9v0BEHKMAKPdz',
        'https://youtu.be/IrAfjW5qiyo?si=JGagzA1iVU975nDz',
        'https://youtu.be/SvhmaNlLgRM?si=phy8SmKFPaKqeXt0',
        'https://youtu.be/EGwernNsL68?si=QA0xejvwt9j6MXhC',
        'https://youtu.be/CWWO_VcdnHY?si=1gIBPw7YMuvdE4D4',
        'https://youtu.be/Wu_kYUA5MGo?si=Ypr3Os4gf4lBkQrw'
    ],

    'metal': [
        'https://youtu.be/AkFqg5wAuFk?si=Gh5zLHhoUo9fRDaB',
        'https://youtu.be/y3Whz4iBYqg?si=DiTVGm3DOT1WRFiy',
        'https://youtu.be/2wYnAYfGgTg?si=xkGuZcDJgFtYSIb_',
        'https://youtu.be/uNi0tsCU-6g?si=R0R1Hjw52Aie-VON'
    ],

    'pop': [
        'https://youtu.be/JJ7mogqDXOw?si=FjQhIoLKZppDOlKg',
        'https://youtu.be/KGVh_eg1Ctg?si=RzbrAyufJeBkBZOQ',
        'https://youtu.be/5NV6Rdv1a3I?si=LgNrnmds2tjJyNdc',
        'https://youtu.be/bESGLojNYSo?si=pR8Ny5-oFaau2H9B',
        'https://youtu.be/euCqAq6BRa4?si=Deg1bfqADp6Im3gn',
        'https://youtu.be/bnVUHWCynig?si=Zn6CzUOkmde09mPE',
        'https://youtu.be/e-ORhEE9VVg?si=q3oe2gktgt3WTRsL'
    ],

    'reggae': [
        'https://youtu.be/hzqFmXZ8tOE?si=DBP_R4lMmz9OZL1t',
        'https://youtu.be/LfeIfiiBTfY?si=X6sekNZIVrZ_YFpS',
        'https://youtu.be/tvy5TGLUls8?si=S4aWW36f7mNmra79'
    ],

    'rock': [
        'https://youtu.be/ma9I9VBKPiw?si=GJf1UJ-TnHaBU_Wf',
        'https://youtu.be/so23_c7lXno?si=3gsEg9_eY51Ncwwg',
        'https://youtu.be/pAgnJDJN4VA?si=jelTlxdnzQgK7rUa',
        'https://youtu.be/ZhIsAZO5gl0?si=7zPvW_SGqG8Ei6Nn',
        'https://youtu.be/l482T0yNkeo?si=BKG6cmAOQE84p22L'
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
# {
#     'blues': [
#         'https://youtu.be/71Gt46aX9Z4?si=cOn0txabywviFeQc',
#         'https://youtu.be/Rj_NUS9hwxA?si=y133TLuYyaUQ_Sjc',
#         'https://youtu.be/ccHrgxsO9z0?si=XSxYT-dscaO5b-vW',
#         'https://youtu.be/rnQzXv-bbkY?si=LT0SNCqqpw-T2Csf'
#     ],
#     'classical': [
#         'https://www.youtube.com/watch?v=_4IRMYuE1hI',
#         'https://www.youtube.com/watch?v=i2e_o4i5WbM',
#         'https://www.youtube.com/watch?v=drwfplnOf4o',
#         'https://www.youtube.com/watch?v=qBP5Qyxowug',
#         'https://youtu.be/5hTvc3f83Ws?si=jN642Yev9t-CtQpa'
#     ],
#     'country': [
#         'https://youtu.be/CpkZfkxdj2c?si=oUFdE8KYQ1hMNjbU',
#         'https://youtu.be/J1glRjDruo0?si=AAa20dY-Z4eEAWoN',
#         'https://youtu.be/L6qMLN34Irw?si=gS3QtKJTG0qbi55r',
#         'https://youtu.be/ZJL4UGSbeFg?si=Xr3QFiG0Ev3srpi2',
#         'https://youtu.be/8N2k-gv6xNE?si=1HLwzDpTGfHaxrWz'
#     ],
#     'disco': [
#         'https://youtu.be/oMVe_HcyP9Y?si=YiZfqd2q_y1WPNdQ',
#         'https://youtu.be/-ihs-vT9T3Q?si=zDH48U7CKF7iObNm',
#         'https://youtu.be/tIt-WiNkB8g?si=6SZhrUQepixMHBQr',
#         'https://youtu.be/qchPLaiKocI?si=CNBZR7exZQVbVfAT'
#     ],
#     'hiphop': [
#         'https://www.youtube.com/watch?v=rNeJW6OaeCY',
#         'https://www.youtube.com/watch?v=LM13e6b76_A',
#         'https://youtu.be/7D_JwgIM-y4?si=xOorFP0OCtJ-m5so',
#         'https://www.youtube.com/watch?v=dFZPClAiW40,'
#         'https://www.youtube.com/watch?v=cq2paBCLSSc'
#
#     ],
#     'jazz': [
#         'https://www.youtube.com/watch?v=ylXk1LBvIqU',
#         'https://youtu.be/fsJ3JjpZyoA?si=cOCXrur_KsnKr33F',
#         'https://youtu.be/CpB7-8SGlJ0?si=L35DmI5cXWEJ9nBM'
#     ],
#     'metal': [
#         'https://www.youtube.com/watch?v=b3-QqGVt-tM',
#         'https://www.youtube.com/watch?v=pAgnJDJN4VA',
#         'https://www.youtube.com/watch?v=tMDFv5m18Pw',
#         'https://www.youtube.com/watch?v=9erLsEHAZRI',
#         'https://www.youtube.com/watch?v=p9SHMeUhTps'
#     ],
#     'pop': [
#         'https://youtu.be/DUT5rEU6pqM?si=-UZlG_a5jvAFXZc2',
#         'https://youtu.be/c18441Eh_WE?si=GfnN_so7Wswz37mk',
#         'https://youtu.be/elueA2rofoo?si=GCIDc6qI5v1B_UuY',
#         'https://www.youtube.com/watch?v=1__CAdTJ5JU',
#         'https://www.youtube.com/watch?v=mgT0N3tMP74'
#     ],
#     'reggae': [
#         'https://youtu.be/K6oYyG0KcvQ?si=guFpGfhvQSEdvzoE',
#         'https://youtu.be/w-wkxoKWgWY?si=YMXJtLUpk_vSyzV6',
#         'https://youtu.be/Jk4RLyFNDi8?si=5GtSFttn2bNQKVjC',
#         'https://youtu.be/H3yhnXwSk7Y?si=JXoy0DKKEXQwYgZQ'
#
#     ],
#     'rock': [
#         'https://youtu.be/Aiay8I5IPB8?si=6vta4YsCYOSHpyam',
#         'https://youtu.be/0J2QdDbelmY?si=ogSmO7abbMSas9Cb',
#         'https://youtu.be/r00ikilDxW4?si=Z2HYkTIPe5XPTHDW',
#         'https://www.youtube.com/watch?v=vyzO-5vt48g'
#     ],
# }
