import pandas as pd
import numpy as np
import pymongo
import duckdb
import ast
from difflib import SequenceMatcher


def load_job_data():
    myclient = pymongo.MongoClient("mongodb://mongoadmin:admin@13.67.48.201:27017/")
    mydb = myclient["LinkedIn"]

    # Get job skills
    mycol = mydb["JobsSkills2"]
    cursor = mycol.find()
    items = list(cursor)
    df1 = pd.DataFrame(items)

    # Get job title
    mycol = mydb["JobsDescription"]
    cursor = mycol.find()
    items = list(cursor)
    df3 = pd.DataFrame(items)
    df3 = df3[['_id','jobTitle']]

    df_temp = duckdb.query("SELECT df1._id as job_id,df1.skills,df3.jobTitle FROM df1,df3 WHERE df1._id = df3._id").df()

    # Load job_id, skills, job_title into dataframe with type 'list'
    df_job = df_temp[['job_id','jobTitle']]
    column_skills = []
 
    for i in range(0,len(df_temp)):
        x = ast.literal_eval(df_temp.iloc[i]['skills'])
        column_skills.append(x)
    df_job['skills'] = column_skills

    return df_job


def load_user_data():
    myclient = pymongo.MongoClient("mongodb://mongoadmin:admin@13.67.48.201:27017/")
    mydb = myclient["LinkedIn"]
    # Get user skills
    mycol = mydb["Users_profile"]
    cursor = mycol.find()
    items = list(cursor)
    df_user = pd.DataFrame(items)
    # Load table Users with _id, user_vector, experience into dataframe with type 'list'
    for i in range(0,len(df_user)):
        df_user.iloc[i]['user_vector'] = ast.literal_eval(df_user.iloc[i]['user_vector'])
        df_user.iloc[i]['experience'] = ast.literal_eval(df_user.iloc[i]['experience'])
    return df_user

def jaccard_similarity(A:list, B:list):
    #Find intersection of two sets
    X = set(A)
    Y = set(B)

    if len(X) == 0:
        return 0,X
    nominator = X.intersection(Y)

    #Find union of two sets
    denominator = X.union(Y)

    #Take the ratio of sizes
    # similarity = len(nominator)/len(X)
    similarity = len(nominator)    
    return similarity,nominator


def domain_comparison(jobTitle = '',user_exp = list):
    list_ratio =[]
    if len(user_exp) == 0:
        list_ratio.append(0)
    else:
        for item in user_exp:
            ratio = SequenceMatcher(None, item, jobTitle).ratio()
            list_ratio.append(ratio)
    return max(list_ratio)


def general_similarity(skill_similarity,domain_similarity):
    score = skill_similarity * 0.7 + domain_similarity * 0.3
    # score = skill_similarity
    return score




def recommend(user_exp:list,user_vector:list,df_job:pd.DataFrame):
    # Get job skills
    df4 = df_job.copy()
    list_similarity = []
    list_of_skills = []

    # Loop calculate similarity
    for i in range (0,len(df4)):
        job_vector = df_job.iloc[i]['skills']
        job_title = df_job.iloc[i]['jobTitle']
        
        # print('JOB TITLE: ',job_title)
        # print('USER VECTOR: ',type(test_user['experience']))
        jaccard_score,skills = jaccard_similarity(job_vector,user_vector)
        domain_score = domain_comparison(job_title,user_exp)
        # print('domain_score: ',domain_score)

        list_similarity.append(general_similarity(jaccard_score,domain_score))
        list_of_skills.append(skills)
    df4['similarity'] = list_similarity
    df4['skills_match'] = list_of_skills

    # Return top 10 job
    result = duckdb.query("SELECT * FROM df4 ORDER BY similarity DESC LIMIT 10").df()
    return result



def recommend_top_N(user_exp:list,user_vector:list,df_job:pd.DataFrame,N):
    # Get job skills
    df4 = df_job.copy()
    list_similarity = []
    list_of_skills = []

    # Loop calculate similarity
    for i in range (0,len(df4)):
        job_vector = df_job.iloc[i]['skills']
        job_title = df_job.iloc[i]['jobTitle']
        
        # print('JOB TITLE: ',job_title)
        # print('USER VECTOR: ',type(test_user['experience']))
        jaccard_score,skills = jaccard_similarity(job_vector,user_vector)
        domain_score = domain_comparison(job_title,user_exp)
        # print('domain_score: ',domain_score)

        list_similarity.append(general_similarity(jaccard_score,domain_score))
        list_of_skills.append(skills)
    df4['similarity'] = list_similarity
    df4['skills_match'] = list_of_skills

    # Return top 10 job
    result = duckdb.query("SELECT * FROM df4 ORDER BY similarity DESC LIMIT " + str(N)).df()
    return result





def max_similarity(user_exp:list,user_vector:list,df_job:pd.DataFrame):
    # Get job skills
    df4 = df_job.copy()
    list_similarity = []
    list_of_skills = []

    # Loop calculate similarity
    for i in range (0,len(df4)):
        job_vector = df_job.iloc[i]['skills']
        job_title = df_job.iloc[i]['jobTitle']
        
        # print('JOB TITLE: ',job_title)
        # print('USER VECTOR: ',type(test_user['experience']))
        jaccard_score,skills = jaccard_similarity(job_vector,user_vector)
        domain_score = domain_comparison(job_title,user_exp)
        # print('domain_score: ',domain_score)

        list_similarity.append(general_similarity(jaccard_score,domain_score))
    return max(list_similarity)




def EDA_tile(df_job:pd.DataFrame,input=''):
    df_DE = df_job.copy()
    list_temp = []
    for i in range(len(df_DE)):
        if input.lower() in df_DE.iloc[i]['jobTitle'].lower():
            list_temp = list_temp + df_DE.iloc[i]['skills']
    dfx = pd.DataFrame(list_temp,columns=['item'])

    keys = dfx['item'].value_counts()[:40].index.tolist()
    values = dfx['item'].value_counts()[:40].tolist()
    return keys,values

def EDA_user_role(df_user:pd.DataFrame,input=''):
    df = df_user.copy()
    total_user_skills = []
    for i in range(0,len(df)):
        exp_list = df.iloc[i]['experience']
        for item in exp_list:
            if input.lower() in item.lower():
                total_user_skills = total_user_skills + df.iloc[i]['user_vector']
                break
    dfx = pd.DataFrame(total_user_skills,columns=['item'])

    keys = dfx['item'].value_counts()[:20].index.tolist()
    values = dfx['item'].value_counts()[:20].tolist()
    return keys, values


def user_job_score(test_user:dict,job_title,job_vector:list):
    jaccard_score,skills = jaccard_similarity(job_vector,test_user['user_vector'])
    domain_score = domain_comparison(job_title,test_user['experience'])
    overall_score = general_similarity(jaccard_score,domain_score)
    return overall_score,skills

def compare_users_1JD(user1_vector:dict,user2_vector:dict, job_title,job_vector:list):
    user1_score,user1_match_skills = user_job_score(user1_vector,job_title,job_vector)
    user2_score,user2_match_skills = user_job_score(user2_vector,job_title,job_vector)
    print("USER 1 Score: ",user1_score,user1_match_skills)
    print("USER 2 Score: ",user2_score,user2_match_skills)
    # list_user = []
    return user1_score,user1_match_skills,user2_score,user2_match_skills



def main():
    df_job = load_job_data()
    df_user = load_user_data()
    df_result = recommend(df_user.iloc[56]['experience'],df_user.iloc[56]['user_vector'],df_job)
    print(df_result)

# main()