import keras

from consts import SEGMENT_DURATION, DATA_JSON_FILE_NAME, MODEL_TEST_NAME, WITH_TEMPO
from learn.load_json_data import DataSet, prepare_datasets


def build_model(input_shape, lstm_1, lstm_2, dense, dropout):
    model = keras.Sequential()

    # warstwy LSTM
    model.add(keras.layers.LSTM(lstm_1, input_shape=input_shape, return_sequences=True))
    model.add(keras.layers.LSTM(lstm_2))

    model.add(keras.layers.Dense(dense, activation='relu'))

    model.add(keras.layers.Dropout(dropout))
    model.add(keras.layers.Dense(10, activation='softmax'))

    return model


def run(data_set: DataSet,
        epochs=75,
        batch_size=32,
        learning_rate=0.001,
        lstm_1=64,
        lstm_2=64,
        dense=64,
        dropout=0.3):
    inputs_train = data_set.inputs_train
    inputs_validation = data_set.inputs_validation
    inputs_test = data_set.inputs_test
    targets_train = data_set.targets_train
    targets_validation = data_set.targets_validation
    targets_test = data_set.targets_test
    input_shape = (inputs_train.shape[1], inputs_train.shape[2])

    model = build_model(input_shape, lstm_1, lstm_2, dense, dropout)

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(optimizer=optimizer,
                  loss=keras.losses.sparse_categorical_crossentropy,
                  metrics=["accuracy"])

    model.summary()

    # wyuczenie modelu
    history = model.fit(inputs_train, targets_train,
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
        'model': model,
        'with_tempo': WITH_TEMPO,
        'segment_duration': SEGMENT_DURATION
    }


if __name__ == '__main__':
    data_set = prepare_datasets(0.25, 0.2, json_path='../{}'.format(DATA_JSON_FILE_NAME))
    train_data = run(data_set, epochs=75)
    train_data["model"].save('{}'.format(MODEL_TEST_NAME))
