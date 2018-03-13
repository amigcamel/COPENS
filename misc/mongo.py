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
