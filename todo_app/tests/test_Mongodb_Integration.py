import mongomock
import pytest
import pymongo
import os
from todo_app import app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

# Stub replacement for requests.get(url)
def stub(url, params={}):
    conn_string = os.environ.get('MONGO_CONN_STRING')
    fake_response_data = None
    client = pymongo.MongoClient(conn_string)

    db = client.mrhtodoappdb
    collection = db.todoapp_collection
    posts = db.posts
    post = {
            "status": "To Do",
            "name": "Example",
        }
    fake_response_data = posts.insert_one(post).inserted_id
       
    return StubResponse(fake_response_data)

def test_index_page(client):

    # Make a request to our app's index page
    response = client.get('/')
    
    assert response.status_code == 200
    assert 'To Do' in response.data.decode()