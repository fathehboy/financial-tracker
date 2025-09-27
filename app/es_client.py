# Elasticsearch client setup
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

ES_HOST = os.getenv("ES_HOST")
ES_USER = os.getenv("ES_USER")
ES_PASS = os.getenv("ES_PASS")

es = Elasticsearch(
    ES_HOST,
    http_auth=(ES_USER, ES_PASS)
)
