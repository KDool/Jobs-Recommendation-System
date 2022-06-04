import pandas as pd
from os import listdir
from os.path import isfile, join
import pymongo
import check_mongo

# Read all to DataFrame
def read_and_clean_single_role(input_path=''):
    df = pd.read_csv(input_path,header=None)
    print(df)
    # Drop Null Values for description column
    # df = df.dropna(axis=0,subset=['description'])

    # Remove the same description & company & jobTitle & location & type
    df = df.drop_duplicates(subset=[0],keep='first')

    return df
    
def create_field_DataFrame(input_list = list):
    list_dfs=[]
    for item in input_list:
        print(item)
        df_tmp = read_and_clean_single_role('../../DS/'+item)
        list_dfs.append(df_tmp)

    df = pd.concat(list_dfs)
    df = df.drop_duplicates(subset=[0],keep='first')
    df = df.reset_index()
    return df


def main():
    # Read all files user ID  result
    mypath = '../../DS/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    df_DS = create_field_DataFrame(onlyfiles)
    df_DS.columns = ['index','_id']
    df_DS = df_DS[['_id']]
    list_users = df_DS.to_dict('records')

    myclient = pymongo.MongoClient('mongodb://mongoadmin:admin@13.67.48.201:27017/')
    mydb = myclient["LinkedIn"]
    mycol = mydb["UserIDs"]

    mycol.bulk_write([pymongo.ReplaceOne({'_id':user['_id']},user, upsert=True) for user in list_users])
    # mycol.update_many(list_users,upsert=True)
    # mydoc = mycol.find()
    # result = list(mydoc)
    # print(len(result))
    # temp_list = []
    # count = 0
    # for user in list_users:
    #     print("COUNT: ",count)
    #     count += 1
    #     mycol.update_one(user,upsert=True)
    # mycol.insert_many(list_users,bypass_document_validation=True)


main()