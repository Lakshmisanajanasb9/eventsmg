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

import pytest
from website import create_app, db

@pytest.fixture
def app():
    # Use test config by setting DATABASE_URL before app creation
    import os
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'  # In-memory DB for testing

    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()  # Setup test database

    yield app

    # Teardown
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data
