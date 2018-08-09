from mysite.celery import app
import pymongo
from django.conf import settings
connection = pymongo.MongoClient(settings.MONGO_SERVER, settings.MONGO_PORT)
import json

@app.task
def added_item(item):
    item = json.loads(item)
    db = connection[settings.MONGO_DB_NAME]
    db.authenticate(settings.MONGO_USER_NAME, settings.MONGO_USER_PASSWORD)
    sgc = db.scrapped_goods
    old_obj = sgc.find_one({'ware_name':item['ware_name']})
    if old_obj:
        sgc.update_one({
            '_id': old_obj['_id']
        },{
            '$set': {
                'ware_name': item['ware_name'],
                'price': item['price'],
                'currency': item['currency'],
                'description': item['description'],
                'images': item['images'],
                'brand': item['brand'],
                'sizes': item['sizes'],
            }
        })
    else:
        sgc.insert_one(item)