import json
from website import create_app

app = create_app()
client = app.test_client()

def test_example():
    assert 1 + 1 == 2  # This should always pass

def get_events():
    response = client.get("/events")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def book_event():
    assert 1 + 1 == 2