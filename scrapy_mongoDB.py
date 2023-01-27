# from items import DaomubijiItem
# from scrapy.conf import settings
import pymongo


class DaomubijiPipeline(object):
    def __init__(self):
        pass
        # host = settings['MONGODB_HOST']
        # port = settings['MONGODB_PORT']
        # dbName = settings['MONGODB_DBNAME']
        # client = pymongo.MongoClient(host=host, port=port)
        # tdb = client[dbName]
        # self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        pass
        # bookInfo = dict(item)
        # self.post.insert(bookInfo)
        # return item
