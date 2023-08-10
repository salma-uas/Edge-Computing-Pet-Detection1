FROM python:3.9.16-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY requirements.txt ./

# RUN apt add --update --no-cache --virtual .tmp-build-deps \
#     gcc libc-dev linux-headers musl-dev build-base

RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
# RUN apk del .tmp-build-deps

COPY . .

ENV ENV docker

CMD [ "python", "run.py" ]
