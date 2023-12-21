import redis
import json
import time

import learn_lstm

with redis.Redis() as Client:
    while True:
        problem_json = Client.brpop('learn')[1]
        problem = json.loads(problem_json)
        print(problem)
        time_start = time.time()

        learning_out = learn_lstm.run(**problem)
        time_end = time.time()
        output = {
            **learning_out,
            'time_start': time_start,
            'time_end': time_end
        }
        result = json.dumps(output)
        Client.lpush('results', result)
