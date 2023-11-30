import json
import numpy as np
from sklearn.model_selection import train_test_split
import keras

DATA_PATH = 'data.json'


def load_data(data_path):
    with open(data_path, "r") as fp:
        data = json.load(fp)
    inputs = np.array(data["mfcc"])
    targets = np.array(data["labels"])
    return inputs, targets


inputs, targets = load_data(DATA_PATH)
inputs_train, inputs_test, targets_train, targets_test = train_test_split(inputs,
                                                                          targets,
                                                                          test_size=0.3)




model = keras.Sequential([
    #input
    keras.layers.Flatten(input_shape=(inputs.shape[1], inputs.shape[2])),
    keras.layers.Dense(512, activation="relu"),
    keras.layers.Dense(256, activation="relu"),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

# compile
optimizer = keras.optimizers.Adam(learning_rate=0.0001)

model.compile(optimizer=optimizer,
              loss=keras.losses.sparse_categorical_crossentropy,
              metrics=["accuracy"])

model.summary()


#train
model.fit(inputs_train, targets_train,
          validation_data=(inputs_test, targets_test),
          epochs=50,
          batch_size=32)