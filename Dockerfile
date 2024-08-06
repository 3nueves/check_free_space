ARG VERSION_PYTHON="3.10.6-slim-buster"

FROM python:${VERSION_PYTHON}

ENV PYTHONUTNBUFFERED 1

LABEL verion="1.0.0" \
    team="devops"

RUN apt-get update -y && apt-get install -y python3-dev gcc \
    build-essential pipenv locales locales-all vim \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -s /bin/bash check

WORKDIR /app

VOLUME [ "/var/log" ]

COPY Pipfile* ./

RUN set -ex && pipenv install --deploy --system

COPY . /app

RUN chown check /app/check_free_space.py

USER  check

CMD [ "/usr/local/bin/python3", "-u", "/app/check_free_space.py" ]