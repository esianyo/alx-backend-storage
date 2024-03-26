#!/usr/bin/env python3
"""insert schools"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """This function inserts a new document in a collection based on kwargs"""
    doc = mongo_collection.insert_one(kwargs)
    return doc.inserted_id
