import json
import time

from pymongo import UpdateOne
from urllib3 import PoolManager
import pymongo

mongo = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo['flyff']

def task_job():
   #this will be used to fetch data on a web site, url is  https://api.flyff.com/
    url = 'https://api.flyff.com/'

    #fetch_items_ids(url)
    #fetch_items_data(url)







def fetch_items_ids(url):

    url_item = url + 'item'
    http = PoolManager()
    response = http.request('GET', url_item)
    #response should be a json object which contain all id of items available in the game, add them to the database in items collection
    responseJson = json.loads(response.data.decode('utf-8'))

    transformed_items = [{'id': item} for item in responseJson]
    print(len(transformed_items))


    db.items.insert_many(transformed_items)
    print("items added to the database")

def fetch_items_data(url):
    #first get all the ids from items collection
    items = db.items.find({})
    #we can calls https://api.flyff.com/item/{itemIds}, we can pass more than one id but avoid limit of 2048 characters in url
    #there's also a cooldown of 300 request per minute

    #do 100 items per request
    items_ids = [item['id'] for item in items]
    items_ids = [items_ids[i:i + 100] for i in range(0, len(items_ids), 100)]
    print(len(items_ids))

    for ids in items_ids:
        ids_str = [str(id) for id in ids]
        url_items = url + 'item/' + ','.join(ids_str)
        http = PoolManager()
        response = http.request('GET', url_items)
        responseJson = json.loads(response.data.decode('utf-8'))
        bulk_operations = []
        for item in responseJson:
            # Create an UpdateOne operation for each item
            bulk_operations.append(
                UpdateOne(
                    {'id': item['id']},  # Filter to find the document with this ID
                    {'$set': item},  # Update the document with the new data
                    upsert=True  # Insert the document if it does not exist
                )
            )
        if bulk_operations:
            db.items.bulk_write(bulk_operations)

        print("items data updated")
        time.sleep(0.3)




task_job()