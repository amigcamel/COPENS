from django.conf import settings
from pymongo import MongoClient

def mongoDB(db, collection=None):
    client = MongoClient('localhost')
    client.admin.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)
    if collection:
        output = client[db][collection]
    else:
        output = client[db]
    return output

# This is used for accessing mongodb without authentication
#from pymongo import Connection
#def connect(db, collection):
#       C = Connection(host='localhost', port=27017)
#       output = C[db][collection]
#       C.close()
#       return output
