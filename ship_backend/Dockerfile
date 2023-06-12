FROM python:3.8.16-slim-bullseye as python

RUN apt-get update && apt-get install -y netcat

WORKDIR /usr/local/delivery
COPY requirements.txt .


RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]
