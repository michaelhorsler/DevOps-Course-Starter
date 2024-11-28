from flask.testing import FlaskClient
import mongomock
import pytest

from todo_app import app
from dotenv import load_dotenv, find_dotenv
from todo_app.data.mongo_items import get_post_collection, get_items
from flask_dance.consumer.storage import MemoryStorage
from todo_app.oauth import blueprint


@pytest.fixture
def client(monkeypatch):
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    storage = MemoryStorage({"access_token": "fake-token"})
    monkeypatch.setattr(blueprint, 'storage', storage)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client


def test_index_page(client):

    posts = get_post_collection()
    post = {
            "status": "To Do",
            "name": "Example",
        }
    posts.insert_one(post).inserted_id
  
    # Make a request to our app's index page

    response = client.get('/')
    
    assert response.status_code == 200
    assert 'Example' in response.data.decode()