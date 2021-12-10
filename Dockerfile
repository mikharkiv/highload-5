FROM python:3.8.2

RUN mkdir -p /app/
WORKDIR /app/
RUN MKDIR /app/db/

COPY . ./
RUN pip install -r requirements.txt
