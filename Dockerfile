FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/server

RUN apt-get -y update && \
        apt-get -y install ffmpeg

COPY requirements.txt /app/server

# Build psycopg2-binary from source -- add required required dependencies
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev && \
        pip install --no-cache-dir -r requirements.txt && \
        apk --purge del .build-deps

COPY . /app/server

ENTRYPOINT [ "entrypoint.sh" ]

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]