import json
from collections import defaultdict
from typing import Dict

from multiprocessing.pool import ThreadPool
import redis
from flask import Flask, Response, request

last_ids = defaultdict(lambda: "$")

app = Flask(__name__)
pool = ThreadPool(processes=20)


@app.route("/get-book/<book_name>/", methods=["GET"])
def get_book(book_name):
    async_result = pool.apply_async(async_get_book, (book_name,))
    res = async_result.get()
    return Response(res, status=200 if res else 404)


def async_get_book(book_id):
    if not rds.get(book_id):
        print('Nothing in cache. Asking for book')
        send_event({"type": "get_book", "book_name": book_id}, "1")
        read_event("1")
        print('Got answer from Worker')
    return rds.get(book_id)


@app.route("/add-book/", methods=["POST"])
def add_book():
    book = request.json
    if not isinstance(book, dict) or {"name", "author", "comment"} - set(book.keys()):
        return Response("Invalid data", status=400)
    # Checking if book with same name exists
    if not rds.get(book["name"]):
        async_result = pool.apply_async(async_get_book, (book["name"],))
        if not async_result.get():
            send_event({"type": "add_book", "book": json.dumps(book)}, "1")
            print('Send add_book to Worker')
            return Response(json.dumps(book), status=200)

    return Response(f'Book with name {book["name"]} already exists', status=400)



def send_event(event: Dict, stream: str):
    rds.xadd(stream, event)


def read_event(stream: str):
    events = rds.xread({stream: last_ids[stream]}, block=300_000, count=1)[0][1]
    event_id = events[0][0]
    event_obj = events[0][1]
    last_ids[stream] = event_id
    return event_obj


if __name__ == "__main__":
    rds = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    app.run(host="0.0.0.0", debug=True)
    print("Web STARTED")
