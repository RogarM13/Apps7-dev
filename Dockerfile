FROM python:3.8-slim-buster

ARG APP_PATH=/opt/service

RUN  apt update

WORKDIR $APP_PATH

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY app .
EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
