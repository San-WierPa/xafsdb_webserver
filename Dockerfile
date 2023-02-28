FROM python:3.10-slim-bullseye

RUN pip install --upgrade pip

RUN mkdir /app

COPY webserver /app/webserver

COPY xafsdb_web /app/xafsdb_web

COPY manage.py /app

#COPY auto_dataset_create.py /app

COPY db.sqlite3 /app

COPY scicat_py /app
RUN pip install -e ./app

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt
#RUN pip install -r requirements_create.txt --cache-dir /app/pip_cache --ignore-installed

EXPOSE 8000