import pandas as pd
from os import listdir
from os.path import isfile, join
import pymongo



# Read all to DataFrame
def read_and_clean_single_role(input_path=''):
    df = pd.read_csv(input_path,header=None)
    df = df[[1]].copy()
    # Drop Null Values for description column
    # df = df.dropna(axis=0,subset=['description'])

    # Remove the same description & company & jobTitle & location & type
    df = df.drop_duplicates(subset=[0],keep='first')

    return df
    
def create_field_DataFrame(input_list = list):
    list_dfs=[]
    for item in input_list:
        print(item)
        df_tmp = read_and_clean_single_role('../LinkedIn/jobs_result/'+item)
        list_dfs.append(df_tmp)

    df = pd.concat(list_dfs)
    df = df.drop_duplicates(subset=[0],keep='first')
    df = df.reset_index()
    return df


def main():
    # Read all files user ID  result
    mypath = '../LinkedIn/jobs_result'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    df_DS = create_field_DataFrame(onlyfiles)
    df_DS.columns = ['index','_id']
    df_DS = df_DS[['_id']]
    list_users = df_DS.to_dict('records')

    myclient = pymongo.MongoClient("mongodb://mongoadmin:admin@localhost:27017/")
    mydb = myclient["LinkedIn"]
    mycol = mydb["JobIDs"]
    mycol.insert_many(list_users)


main()