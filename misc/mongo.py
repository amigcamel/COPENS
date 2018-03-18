# -*- coding: utf-8 -*-
from django.conf import settings
from pymongo import MongoClient


def mongoDB(db, collection=None):
    client = MongoClient(settings.MONGO_HOST)
    client.admin.authenticate(
        settings.MONGO_USER, settings.MONGO_PASS)
    if collection:
        output = client[db][collection]
    else:
        output = client[db]
    return output
