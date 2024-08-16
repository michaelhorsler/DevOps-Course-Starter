import os
import pymongo
from pymongo import MongoClient
from todo_app.data.item import Item

conn_string = os.getenv("MONGO_CONN_STRING")
mongodb = os.getenv("MONGODB")
client = MongoClient(conn_string)
db = client[mongodb] # type: ignore
# db = client.mrhtodoappdb
collection = db.todoapp_collection
posts = db.posts

def add_item(title):

    post = {
        "status": "To Do",
        "name": title,
    }
    post_id = posts.insert_one(post).inserted_id
    print(post_id)

def get_items():

    items=[]
 #   for post in posts.find({"status": "To Do"}):
    for post in posts.find():
        item = Item.from_mongodb(post)
        items.append(item)
    print (items)
    return items

def move_item_to_active(item_id):
    filter = { '_id': item_id}
    newvalues = { "$set": { 'status': 'Active' } }
    posts.update_one(filter, newvalues)

def move_item_to_done(item_id):
    filter = { '_id': item_id}
    newvalues = { "$set": { 'status': 'Complete' } }
    posts.update_one(filter, newvalues)
