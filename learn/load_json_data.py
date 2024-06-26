import json
import numpy as np
from sklearn.model_selection import train_test_split

from consts import DATA_JSON_FILE_NAME
from shared.mfcc_creator import add_tempo_to_mfcc

JSON_PATH = "../{}".format(DATA_JSON_FILE_NAME)


class DataSet:
    def __init__(self, inputs_train, inputs_validation, inputs_test, targets_train, targets_validation, targets_test):
        self.inputs_train = inputs_train
        self.inputs_validation = inputs_validation
        self.inputs_test = inputs_test
        self.targets_train = targets_train
        self.targets_validation = targets_validation
        self.targets_test = targets_test


def load_data(data_path=JSON_PATH):
    with open(data_path, "r") as fp:
        data = json.load(fp)
    inputs = np.array(data["mfcc"])
    targets = np.array(data["labels"])

    tempo = np.array(data["tempo"])
    inputs = add_tempo_to_mfcc(inputs, tempo)

    return inputs, targets


def prepare_datasets(test_size, validation_size, json_path=JSON_PATH):
    inputs, targets = load_data(json_path)
    inputs_train, inputs_test, targets_train, targets_test = \
        train_test_split(inputs,
                         targets,
                         test_size=test_size)

    inputs_train, inputs_validation, targets_train, targets_validation = \
        train_test_split(inputs_train,
                         targets_train,
                         test_size=validation_size)

    inputs_train = inputs_train[..., np.newaxis]
    inputs_validation = inputs_validation[..., np.newaxis]
    inputs_test = inputs_test[..., np.newaxis]

    return DataSet(inputs_train, inputs_validation, inputs_test, targets_train, targets_validation, targets_test)
