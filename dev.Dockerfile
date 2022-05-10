FROM python:3.9

RUN pip install pipenv

ENV PROJECT_DIR /app

WORKDIR ${PROJECT_DIR}

RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1-dev -y \
        && pip3 install pyaudio

COPY . .

RUN pipenv install --system --deploy

ENTRYPOINT [ "/bin/bash" ]