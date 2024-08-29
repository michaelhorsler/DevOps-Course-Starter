import os
import pymongo
from todo_app.data.item import Item

def get_post_collection():
    conn_string = os.getenv("MONGO_CONN_STRING")
    mongodb = os.getenv("MONGODB")

    client = pymongo.MongoClient(conn_string)

    db = client[mongodb] # type: ignore

    posts = db.posts
    return posts

def add_item(title):
    posts = get_post_collection()
    post = {
        "status": "To Do",
        "name": title,
    }
    posts.insert_one(post).inserted_id

def get_items():
    posts = get_post_collection()
    items=[]
 #   for post in posts.find({"status": "To Do"}):
    for post in posts.find():
        item = Item.from_mongodb(post)
        items.append(item)
    #print (items)
    return items

def move_item_to_active(item_id):
    posts = get_post_collection()
    filter = { '_id': item_id}
    newvalues = { "$set": { 'status': 'Active' } }
    posts.update_one(filter, newvalues)

def move_item_to_done(item_id):
    posts = get_post_collection()
    filter = { '_id': item_id}
    newvalues = { "$set": { 'status': 'Complete' } }
    posts.update_one(filter, newvalues)
