import json

from web.web import create_app

API_URL = "http://localhost:5000/"


def test_healthcheck_and_add_book():
    app = create_app()
    client = app.test_client()
    assert client.get("/").status_code == 404
    book = {
        "name": "test",
        "author": "test",
        "comment": "test",
    }
    client.post("/add-book/", json=book)
    r = client.get("/get-book/test/")
    assert r.status_code == 200
    assert json.loads(r.data) == book
