from pymongo import MongoClient
from os import environ

db = MongoClient(environ['DATABASE_URL'])