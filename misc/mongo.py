# -*- coding: utf-8 -*-

from pymongo import MongoClient


def mongoDB(db, collection=None):
    client = MongoClient('')
    client.admin.authenticate('',
                              '')
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
