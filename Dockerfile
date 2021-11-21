FROM python:3.9-slim

RUN apt-get update && apt-get install -y python3-pip wget lsb-release libpq-dev
RUN mkdir -p /etc/apt/sources.list.d && touch /etc/apt/sources.list.d/pgdg.list
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get install -y postgresql postgresql-client
RUN pip install sqlalchemy psycopg2 "fastapi[all]"

WORKDIR /app
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app"]