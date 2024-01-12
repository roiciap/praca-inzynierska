class test_song:
    def __init__(self, db_id, name, genre_id, genre_name, mfcc=[]):
        self.id = db_id
        self.name = name
        self.genre_id = genre_id
        self.genre_name = genre_name
        self.mfcc = mfcc

    def set_mfcc(self, mfcc):
        self.mfcc = mfcc
