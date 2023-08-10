FROM --platform=linux/arm64 python:3.9.16-slim-bullseye
# FROM python:3.9.16-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY requirements.txt ./

# RUN apt-get update && apt-get install -y mariadb-dev
# RUN apt-get install mariadb-dev
RUN apt update

# RUN apt update --no-cache --virtual .tmp-build-deps \
#     gcc libc-dev linux-headers musl-dev
RUN pip install --no-cache-dir -r requirements.txt
# RUN apt del .tmp-build-deps

COPY . .

ENV ENV docker

CMD [ "python", "run.py" ]