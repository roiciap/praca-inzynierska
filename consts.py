SAMPLE_RATE = 22050
SEGMENT_DURATION = 6
GENRES_SORTED = ["blues",
                 "classical",
                 "country",
                 "disco",
                 "hiphop",
                 "jazz",
                 "metal",
                 "pop",
                 "reggae",
                 "rock"]

WITH_TEMPO = False

REMOVE_SILENT = True
THRESHOLD_ENERGY = 0.005

DATA_JSON_FILE_NAME = 'experimental-data-{}.json'.format(SEGMENT_DURATION)
MODEL_TEST_NAME = 'experimental-model-{}.h5'.format(SEGMENT_DURATION)
# MODEL_TEST_NAME = 'model-6.h5'.format(SEGMENT_DURATION)



CONFIG_FILE_NAME = 'config.json'
