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

-- Ustaw uprawnienia dla nowego użytkownika na nową tabelę
GRANT ALL ON TABLE learning_analysis.learn_results TO mateuszb;

GRANT USAGE, SELECT ON SEQUENCE learning_analysis.learn_results_id_seq TO mateuszb;
