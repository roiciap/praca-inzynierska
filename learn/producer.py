import json

import redis

from consts import CONFIG_FILE_NAME

inputs = {
    'epochs': {'min': 50, 'max': 50, 'step': 10},
    'learning_rate': {'min': 0.001, 'max': 0.001, 'step': 0.0005},
    'dropout': {'min': 0.3, 'max': 0.3, 'step': 0.05},
    'lstm_1': {'min': 128, 'max': 128, 'step': 32},
    'lstm_2': {'min': 128, 'max': 128, 'step': 32},
    'dense': {'min': 128, 'max': 128, 'step': 32},
}


def generate_numbers(min, max, step):
    numbers = []
    current_value = min

    while round(current_value, 5) <= max:
        numbers.append(round(current_value, 5))
        current_value += step

    return numbers


params_to_run = {key: generate_numbers(**value) for key, value in inputs.items()}

to_run = [{'key': key, 'value': value, 'count': len(value)} for key, value in params_to_run.items()]

params_len = len(to_run)


def calculate_single_level(to_run_data, level=0, curr_obj=None):
    if curr_obj is None:
        curr_obj = {}
    this_level_data = to_run_data[level]

    results = []
    if level == len(to_run_data) - 1:
        for i in this_level_data['value']:
            results.append({**curr_obj, this_level_data['key']: i})
        return results

    else:
        for i in this_level_data['value']:
            this_level_part = {**curr_obj, this_level_data['key']: i}
            results += calculate_single_level(to_run_data, level=level + 1, curr_obj=this_level_part)
        return results


all_params = calculate_single_level(to_run)
print(all_params)

with open('../{}'.format(CONFIG_FILE_NAME), 'r') as file:
    json_content = json.load(file)
    REDIS_HOST = json_content["REDIS_HOST"]
    REDIS_PORT = json_content["REDIS_PORT"]

with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as client:
    for i in all_params:
        data_to_send = json.dumps(i)
        client.lpush('learn', data_to_send)
        client.close()
