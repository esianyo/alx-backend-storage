#!/usr/bin/env python3
"""listing all"""

import pymongo


def list_all(mongo_collection):
    """This function lists all documents in a collection"""
    documents = mongo_collection.find()
    return [doc for doc in documents]
