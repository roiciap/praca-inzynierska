# Wybierz obraz bazowy (może być oficjalny obraz Python)
FROM python:3.8

# Ustaw folder roboczy
WORKDIR /app
# Skopiuj pliki aplikacji do folderu roboczego
COPY ./db_writer/db_writer.py /app

EXPOSE 5000

# Zainstaluj zależności
RUN pip install flask
# RUN pip install flask_ngrok
RUN pip install psycopg2

# Uruchom aplikację
CMD ["python", "db_writer.py"]