FROM python:3.8.2

RUN mkdir -p /app/
WORKDIR /app/
RUN mkdir db

COPY requirements.txt ./
COPY /worker/. ./
RUN pip install -r requirements.txt

CMD ["python", "-u", "worker.py"]