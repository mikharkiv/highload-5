FROM python:3.8.2

RUN mkdir -p /app/
WORKDIR /app/

COPY requirements.txt ./
COPY /web/. ./
RUN pip install -r requirements.txt

CMD ["python", "web.py"]
