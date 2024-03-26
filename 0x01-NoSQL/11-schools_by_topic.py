#!/usr/bin/env python3
"""schools by topic"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """This function returns the list of school having a specific topic"""
    schools = mongo_collection.find({"topics": topic})
    return [school for school in schools]
