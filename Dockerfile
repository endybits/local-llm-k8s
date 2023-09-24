FROM python:3.10

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

COPY ./makefile /api/makefile

RUN make install

COPY ./app /api/app
COPY ./model /api/model

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80" ]