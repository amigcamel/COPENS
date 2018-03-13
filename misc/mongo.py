# -*- coding: utf-8 -*-
import os

from pymongo import MongoClient


def mongoDB(db, collection=None):
    client = MongoClient(os.environ['mongo_host'])
    client.admin.authenticate(
        os.environ['mongo_user'], os.environ['mongo_pass'])
    if collection:
        output = client[db][collection]
    else:
        output = client[db]
    return output
