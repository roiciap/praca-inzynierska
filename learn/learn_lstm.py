import json
import numpy as np
from sklearn.model_selection import train_test_split
import keras

JSON_PATH = "data.json"


def load_data(data_path):
    with open(data_path, "r") as fp:
        data = json.load(fp)
    inputs = np.array(data["mfcc"])
    targets = np.array(data["labels"])

    return inputs, targets


def prepare_datasets(test_size, validation_size):
    inputs, targets = load_data(JSON_PATH)
    # dodaje axis to input sets
    inputs_train, inputs_test, targets_train, targets_test = train_test_split(inputs,
                                                                              targets,
                                                                              test_size=test_size)

    inputs_train, inputs_validation, targets_train, targets_validation = train_test_split(inputs_train,
                                                                                          targets_train,
                                                                                          test_size=validation_size)

    inputs_train = inputs_train[..., np.newaxis]
    inputs_validation = inputs_validation[..., np.newaxis]
    inputs_test = inputs_test[..., np.newaxis]

    return inputs_train, inputs_validation, inputs_test, targets_train, targets_validation, targets_test


def build_model(input_shape, lstm_1, lstm_2, dense, dropout):
    model = keras.Sequential()

    # warstwy LSTM
    model.add(keras.layers.LSTM(lstm_1, input_shape=input_shape, return_sequences=True))
    model.add(keras.layers.LSTM(lstm_2))

    model.add(keras.layers.Dense(dense, activation='relu'))

    model.add(keras.layers.Dropout(dropout))
    model.add(keras.layers.Dense(10, activation='softmax'))

    return model


def run(epochs=75,
        batch_size=32,
        learning_rate=0.001,
        lstm_1=64,
        lstm_2=64,
        dense=64,
        dropout=0.3):
    inputs_train, inputs_validation, inputs_test, targets_train, targets_validation, targets_test = load_data()

    input_shape = (inputs_train.shape[0], inputs_train.shape[1])

    model = build_model(input_shape, lstm_1, lstm_2, dense, dropout)

    # compile
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(optimizer=optimizer,
                  loss=keras.losses.sparse_categorical_crossentropy,
                  metrics=["accuracy"])

    model.summary()

    # train
    hisotry = model.fit(inputs_train, targets_train,
                        validation_data=(inputs_validation, targets_validation),
                        epochs=epochs,
                        batch_size=batch_size)

    train_loss, train_acc = model.evaluate(inputs_train, targets_train, verbose=2)
    print('\nWynik dla uczacego: ', train_acc)
    validation_loss, validation_acc = model.evaluate(inputs_validation, targets_validation, verbose=2)
    print('\nWynik dla walidacyjnego: ', validation_acc)
    test_loss, test_acc = model.evaluate(inputs_test, targets_test, verbose=2)
    print('\nWynik dla testowego: ', test_acc)
    return {
        'epochs': epochs,
        'batch_size': batch_size,
        'learning_rate': learning_rate,
        'lstm_1': lstm_1,
        'lstm_2': lstm_2,
        'dense': dense,
        'dropout': dropout,
        'test_acc': test_acc,
        'train_acc': train_acc,
        'validation_acc': validation_acc,
        'test_acc': test_acc
    }


run(epochs=10)
