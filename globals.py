# import logging
import pymongo
from config import Config
from pymongo.server_api import ServerApi
from datetime import datetime

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s",
#     handlers=[logging.StreamHandler()],
# )
# log = logging.getLogger()


PRIM_DB_URL=Config.MONGO_URI

class Db:
    def __init__(self):
        self.mongo_url = PRIM_DB_URL
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client['cricketinsights']
        self.posts = self.db["posts"]

    def save_post(self, post_data):
        post_data["scraped_at"] = datetime.utcnow().isoformat()
        self.posts.insert_one(post_data)

db = Db()

