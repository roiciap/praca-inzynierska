import redis
import json
import time
import requests

import learn_lstm
from consts import CONFIG_FILE_NAME
from learn.load_json_data import prepare_datasets

with open('../{}'.format(CONFIG_FILE_NAME), 'r') as file:
    json_content = json.load(file)
    REDIS_HOST = json_content["REDIS_HOST"]
    REDIS_PORT = json_content["REDIS_PORT"]
    DB_WRITER_HOST = json_content["DB_WRITER_HOST"]
    WORKER = json_content["WORKER"]

print("przygotowuje dane...")
data_set = prepare_datasets(0.25, 0.2)

tmp_model_file_path = 'model.h5'
print("podłączam się do kolejki...")
with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as Client:
    while True:
        problem_json = Client.brpop('learn')[1]
        problem = json.loads(problem_json)
        print(problem)
        time_start = time.time()

        learning_out = learn_lstm.run(data_set, **problem)
        learning_out["model"].save(tmp_model_file_path)
        time_end = time.time()
        output = {
            **learning_out,
            'time_start': time_start,
            'WORKER': WORKER,
            'time_end': time_end
        }
        del output["model"]
        params = output
        files = {'file': open(tmp_model_file_path, 'rb')}

        response = requests.post('http://{}/upload_model'.format(DB_WRITER_HOST), files=files, params=params)
        print(response.json())
