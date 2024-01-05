import requests

files = {'file': open('./run/app/tmp/jakis-rap.wav', 'rb')}
files2 = {'file': open('./run/app/tmp/jakis-rap.wav', 'rb')}
response = requests.get('http://127.0.0.1:5000/predict', files=files)
response2 = requests.get('http://127.0.0.1:5000/predict', files=files2)
print(response.json())
print(response2.json())
