from keras.saving.save import load_model

from learn.load_json_data import prepare_datasets

model = load_model('../databases/volumes/models/34.h5')
data_set = prepare_datasets(0.25, 0.2)

train_loss, train_acc = model.evaluate(data_set.inputs_train, data_set.targets_train, verbose=2)
print('\nWynik dla uczacego: ', train_acc)
validation_loss, validation_acc = model.evaluate(data_set.inputs_validation, data_set.targets_validation, verbose=2)
print('\nWynik dla walidacyjnego: ', validation_acc)
test_loss, test_acc = model.evaluate(data_set.inputs_test, data_set.targets_test, verbose=2)
print('\nWynik dla testowego: ', test_acc)
