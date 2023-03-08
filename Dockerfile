FROM python:3.9.0

RUN pip install --upgrade pip

RUN mkdir /app
RUN mkdir -p /app/temp
RUN mkdir -p /app/pip_cache

COPY webserver /app/webserver

COPY xafsdb_web /app/xafsdb_web

COPY manage.py /app

COPY db.sqlite3 /app

COPY scicat_py /app
RUN pip install -e ./app

COPY .env /app
COPY auto_dataset_create.py /app
COPY plugins /app/plugins
COPY quality_control /app/quality_control

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt --cache-dir /app/pip_cache --ignore-installed

EXPOSE 8000