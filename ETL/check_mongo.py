import pandas as pd
import pymongo

def connect():
    url='mongodb://mongoadmin:admin@13.67.48.201:27017/'
    myclient = pymongo.MongoClient(url)
    return myclient

def check_id_exist(input='',db='',collection = ''):
    # Existed -> 1
    # Not existed --> 0
    myclient=connect()
    mydb = myclient[db]
    mycol = mydb[collection]

    query = {'_id':input}
    mydoc = mycol.find(query)
    result = list(mydoc)
    if (len(result)!=0):
        # Exist ID --> dont store to db
        return 1
    else:
        return 0


if __name__=='__main__':
    url='mongodb://mongoadmin:admin@13.67.48.201:27017/'
    myclient = pymongo.MongoClient(url)
    mydb = myclient['LinkedIn']
    mycol = mydb['UserIDs']
    mydoc = mycol.find()
    result = list(mydoc)
    print(len(result))
#     a = check_id_exist('huu-dung','LinkedIn','UserIDs')
#     print(a)