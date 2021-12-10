import json
from collections import defaultdict
from typing import Dict

import redis
import sqlite3

last_ids = defaultdict(lambda: "$")
conn = sqlite3.connect("./db/books.sqlite3")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        `bname` TEXT,
        author TEXT,
        comment TEXT);
""")
conn.commit()


def process_event(event):
    if event["type"] == "add_book":
        print('Adding book')
        book = json.loads(event["book"])
        rds.set(book["name"], json.dumps(book))
        cursor.execute("INSERT INTO books (bname, author, comment) VALUES (?,?,?);",
                           [book['name'], book['author'], book['comment']])
        conn.commit()
    elif event["type"] == "get_book":
        if not event.get("book_name"):
            return
        name = event["book_name"]
        cursor.execute(f"SELECT bname, author, comment FROM books WHERE bname = '{name}'")
        data = cursor.fetchall()
        if data:
            print('Got book from DB. Writing to cache')
            rds.set(name, json.dumps({
                "name": data[0][0],
                "author": data[0][1],
                "comment": data[0][2],
            }))
        else:
            rds.set(event["book_name"], "")
    send_event({"type": event["type"]}, "1")


def send_event(event: Dict, stream: str):
    rds.xadd(stream, event)


def read_event(stream: str):
    events = rds.xread({stream: last_ids[stream]}, block=300_000, count=1)[0][1]
    event_id = events[0][0]
    event_obj = events[0][1]
    last_ids[stream] = event_id
    return event_obj


if __name__ == '__main__':
    rds = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    print("Worker STARTED")
    while True:
        process_event(read_event("1"))

