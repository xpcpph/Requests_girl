import pymongo

mymongodn = pymongo.MongoClient('mongodb://localhost:27017/')
print(mymongodn)
mymongodn1 = mymongodn["runoobdb"]