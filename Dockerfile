FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get -y update \
        && apt-get -y install ffmpeg \
        && apt-get -y install libmagic1 \
        && apt-get install -y --no-install-recommends build-essential libpq-dev \  
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
        && rm -rf /tmp/requirements.txt \
        #&& useradd -U app_user \
        #&& install -d -m 0755 -o app_user -g app_user /app/static
WORKDIR /app/server

#USER app_user:app_user
#COPY --chown=app_user:app_user . .
COPY . .

RUN chmod +x ./*.sh