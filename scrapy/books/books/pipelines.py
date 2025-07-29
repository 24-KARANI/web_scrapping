import pymongo
import hashlib
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class MongoPipeline:
    COLLECTION_NAME = "books"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )
        
    def open_spider(self, spider):
        self.client =pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()
        
    
    """
    # drop duplicate items
    def process_item(self, item, spider):
        item_id = self.compute_item_id(item)
        if self.db[self.COLLECTION_NAME].find_one({"_id": item_id}):
            raise DropItem(f"Duplicate item found: {item}")
        else:
            item["_id"] = item_id
            self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())
        return item
        
    """
    
    # upsert item into MongoDB
    def proess_item(self, item, spider):
        item_id = self.compute_item_id(item)
        item_dict = ItemAdapter(item).asdict()

        self.db[self.COLLECTION_NAME].update_one(
            filter={"_id": item_id},
            update={"$set": item_dict},
            upsert=True
        )
    

    def compute_item_id(self, item):
        url = item["url"]
        return hashlib.sha256(url.encode("utf-8")).hexdigest()
        
class BooksPipeline:
    def process_item(self, item, spider):
        return item
