FROM python:3.10-slim-bullseye

RUN pip install --upgrade pip

RUN mkdir /app

COPY webserver /app/webserver

COPY xafsdb_web /app/xafsdb_web

COPY manage.py /app/

COPY scicat_py /app
RUN pip install -e ./app

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "webserver.asgi:application" ]