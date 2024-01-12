-- setup.sql

-- Utwórz nowego użytkownika
CREATE USER mateuszb WITH PASSWORD 'mbazior';

-- Utwórz nowy schemat
CREATE SCHEMA learning_analysis;

-- Ustaw uprawnienia dla nowego użytkownika na nowy schemat
GRANT ALL ON SCHEMA learning_analysis TO mateuszb;

-- Utwórz nową tabelę w nowym schemacie
CREATE TABLE learning_analysis.learn_results (
    id SERIAL PRIMARY KEY,
    epochs INTEGER,
    batch_size INTEGER,
    learning_rate DOUBLE PRECISION,
    lstm_1 INTEGER,
    lstm_2 INTEGER,
    dense INTEGER,
    dropout DOUBLE PRECISION,
    test_acc DOUBLE PRECISION,
    train_acc DOUBLE PRECISION,
    validation_acc DOUBLE PRECISION,
    time_start TIMESTAMP,
    time_end TIMESTAMP,
    WORKER TEXT,
    segment_duration INTEGER,
    with_tempo BOOLEAN
);

CREATE TABLE learning_analysis.genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE learning_analysis.song (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    genre_id INTEGER REFERENCES learning_analysis.genre(id)
);

CREATE TABLE learning_analysis.song_genre_for_model (
    model_id INTEGER REFERENCES learning_analysis.learn_results(id),
    song_id INTEGER REFERENCES learning_analysis.song(id),
    genre_id INTEGER REFERENCES learning_analysis.genre(id),
    prediction DOUBLE PRECISION
);


-- Ustaw uprawnienia dla nowego użytkownika na nową tabelę
GRANT ALL ON TABLE learning_analysis.learn_results TO mateuszb;
GRANT ALL ON TABLE learning_analysis.genre TO mateuszb;
GRANT ALL ON TABLE learning_analysis.song TO mateuszb;
GRANT ALL ON TABLE learning_analysis.song_genre_for_model TO mateuszb;



GRANT USAGE, SELECT ON SEQUENCE learning_analysis.learn_results_id_seq TO mateuszb;
GRANT USAGE, SELECT ON SEQUENCE learning_analysis.genre_id_seq TO mateuszb;
GRANT USAGE, SELECT ON SEQUENCE learning_analysis.song_id_seq TO mateuszb;
