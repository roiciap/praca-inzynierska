import redis
import json
import time
import requests

import learn_lstm
from learn.load_json_data import prepare_datasets

data_set = prepare_datasets(0.25, 0.2)

model_file_path = 'model.h5'

with redis.Redis() as Client:
    while True:
        problem_json = Client.brpop('learn')[1]
        problem = json.loads(problem_json)
        print(problem)
        time_start = time.time()

        learning_out = learn_lstm.run(data_set, **problem)
        learning_out["model"].save(model_file_path)
        time_end = time.time()
        output = {
            **learning_out,
            'time_start': time_start,
            'time_end': time_end
        }
        del output["model"]
        params = output
        files = {'file': open(model_file_path, 'rb')}

        response = requests.post('http://127.0.0.1:5000/upload_model', files=files, params=params)
        print(response.json())
