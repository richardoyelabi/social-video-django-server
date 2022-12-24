FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/server

RUN apt-get -y update \
        && apt-get -y install ffmpeg \
        && apt-get install -y --no-install-recommends build-essential libpq-dev \  
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/server

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/server

RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]