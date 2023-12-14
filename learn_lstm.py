import json
import numpy as np
from sklearn.model_selection import train_test_split
import keras
import matplotlib.pyplot as plt

DATA_PATH = 'data.json'


def load_data(data_path):
    with open(data_path, "r") as fp:
        data = json.load(fp)
    inputs = np.array(data["mfcc"])
    targets = np.array(data["labels"])

    return inputs, targets


def prepare_datasets(test_size, validation_size):
    inputs, targets = load_data(DATA_PATH)
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


def build_model(input_shape):
    model = keras.Sequential()

    # warstwy LSTM
    model.add(keras.layers.LSTM(64, input_shape=input_shape, return_sequences=True))
    model.add(keras.layers.LSTM(64))

    # dense layer
    model.add(keras.layers.Dense(64, activation='relu'))

    model.add(keras.layers.Dropout(0.3))

    model.add(keras.layers.Dense(10, activation='softmax'))

    return model


def plot_history(history):
    """Plots accuracy/loss for training/validation set as a function of the epochs

        :param history: Training history of model
        :return:
    """

    fig, axs = plt.subplots(2)

    # create accuracy sublpot
    axs[0].plot(history.history["accuracy"], label="train accuracy")
    axs[0].plot(history.history["val_accuracy"], label="test accuracy")
    axs[0].set_ylabel("Accuracy")
    axs[0].legend(loc="lower right")
    axs[0].set_title("Accuracy eval")

    # create error sublpot
    axs[1].plot(history.history["loss"], label="train error")
    axs[1].plot(history.history["val_loss"], label="test error")
    axs[1].set_ylabel("Error")
    axs[1].set_xlabel("Epoch")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Error eval")

    plt.show()

inputs_train, inputs_validation, inputs_test, targets_train, targets_validation, targets_test = prepare_datasets(0.25,
                                                                                                                 0.2)
input_shape = (inputs_train.shape[1], inputs_train.shape[2])

model = build_model(input_shape)

# compile
optimizer = keras.optimizers.Adam(learning_rate=0.001)

model.compile(optimizer=optimizer,
              loss=keras.losses.sparse_categorical_crossentropy,
              metrics=["accuracy"])

model.summary()

# train
hisotry = model.fit(inputs_train, targets_train,
                    validation_data=(inputs_validation, targets_validation),
                    epochs=75,
                    batch_size=32)

test_loss, test_acc = model.evaluate(inputs_test, targets_test, verbose=2)
print('\nWynik dla testowego: ', test_acc)
