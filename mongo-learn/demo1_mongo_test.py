from pymongo import MongoClient

client = MongoClient("mongodb://bitcs:huajian2017@124.193.169.159:54016/?authSource=admin")
database = client["crawl"]
collection = database["CrawlHtmlSource"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

query = {}

cursor = collection.find(query)
try:
    for doc in cursor:
        print(doc["_id"])
finally:
    cursor.close()