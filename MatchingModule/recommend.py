import pandas as pd
import numpy as np
import pymongo
import duckdb
import ast
from difflib import SequenceMatcher



def load_full_JDs():
    myclient = pymongo.MongoClient("mongodb://mongoadmin:admin@13.67.48.201:27017/")
    mydb = myclient["LinkedIn"]
    mycol = mydb["JobsDescription"]
    cursor = mycol.find()
    items = list(cursor)
    df_jobs = pd.DataFrame(items)
    myclient.close()
    return df_jobs

def load_full_Users():
    myclient = pymongo.MongoClient("mongodb://mongoadmin:admin@13.67.48.201:27017/")
    mydb = myclient["LinkedIn"]
    # Get job skills
    mycol = mydb["User_experience"]
    cursor = mycol.find()
    items = list(cursor)
    df_user = pd.DataFrame(items)
    myclient.close()
    return df_user


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
    myclient.close()
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

####################################

MAX_SCORE = 11.98

def filter_threshold(df: pd.DataFrame, threshold=0.2):
    threshold_score = MAX_SCORE * threshold
    dfx = df[df['similarity']>threshold_score]
    # print(dfx)
    return dfx


#####################################
# Analyze Job Locations

import collections

def filter_location(text=''):
    l1 = list(set(text.split(',')))
    r = []
    for i in range(0,len(l1)):
        l1[i] = l1[i].strip().lower()
    l1 = list(set(l1))
    for i in range(0,len(l1)):
        if '/' not in l1[i]:
            r.append(l1[i])
    # print("L1: ",r)
    return r

# filter_location('Hanoi Capital Region')

def EDA_on_location(df:pd.DataFrame):
    df_x = df.copy()
    temp_location = []
    for i in range(0,len(df_x)):
        text = df.iloc[i]['location']
        temp_location.append(filter_location(text))
    df_x['filter_location'] = temp_location
    list_of_types = []

    for i in range (0, len(df_x)):
        list_of_types += df_x.iloc[i]['filter_location']
    dict_result = dict(collections.Counter(list_of_types))
    # print(dict_result)
    keys = list(dict_result.keys())
    values = list(dict_result.values())
    return keys,values
    
#####################################################
# Analyze Job Working Type
def filter_workingType(text=''):
    l1 = list(set(text.split('·')))
    r = []
    for i in range(0,len(l1)):
        l1[i] = l1[i].strip().lower()
    l1 = list(set(l1))
    for i in range(0,len(l1)):
        if '/' not in l1[i]:
            r.append(l1[i])
    # print("L1: ",r)
    return r

def process_DfWorkingType(df:pd.DataFrame):
    column_types = []
    df_x = df.copy()
    for i in range(0, len(df)):
        column_types.append(filter_workingType(df_x.iloc[i]['type']))
    df_x['working'] = column_types
    return df_x

def EDA_on_working(df:pd.DataFrame):
    df_job = df.copy()
    df_x = process_DfWorkingType(df_job)
    list_of_types = []
    for i in range (0, len(df_x)):
        list_of_types += df_x.iloc[i]['working']
    dict_result = dict(collections.Counter(list_of_types))
    # print(dict_result)
    keys = list(dict_result.keys())
    values = list(dict_result.values())
    return keys,values
########################################################
# EDA by Year in Experience




import collections
import re
def compute_months(text=''):
    # calculate months experience from string
    total_months = 0
    check_year = 'yr' in text
    check_month = 'mo' in text
    test_list = text.replace('yr','').replace('mo','').replace('s','').split(' ')
    res = []
    for val in test_list:
        if val != '' and val.isnumeric() :
            # print(val)
            res.append(int(val))
        
    # print(res)
    # print("Check Month: ",check_month)
    # print("Check Year: ",check_year)
        # print(text,len(text))
    if check_year == True and check_month == True:
        total_months = res[0]*12 + res[1]
    elif check_year == True and check_month == False:
        total_months = res[0]*12
    elif check_year == False and check_month == True:
        total_months = res[0]
    else:
        total_months = 0
    return total_months

def EDA_workingexp(df_user:pd.DataFrame):
    column_months = []
    for i in range (0,len(df_user)):
        if len(df_user.iloc[i]['experience']) >0 :
            exp_list = df_user.iloc[i]['experience']
            sum = 0
            for j in range(len(exp_list)):
                s = exp_list[j]
                l = s.split('·')[-1].split(',')[0].strip()
                # regex_check = re.search('(([0-9])* yr(s)* *)*([0-9]+ mos*)*', l)
                if l[0] >= '0' and l[0] <= '9' and (l[1].isalpha()==False):
                    months_exp = compute_months(l)
                    sum = sum + months_exp
                    sum += 0
            if sum > (12*60):
                column_months.append('Others')
            else:
                column_months.append(sum/12)
            # print(l)
        else:
            column_months.append('Others')

    dict_result = dict(collections.Counter(column_months))
    records_NaN = {'Others':dict_result['Others']}
    # print(records_NaN)
    dict_result.pop('Others')


    dictionary_histogram = {}
    for i in range (0,12):
        bin_name = str(5*i) + '-' + str(5*i+5)
        print(bin_name)
        dictionary_histogram[bin_name] = 0

    dictionary_histogram['Others'] = records_NaN['Others']

    key_values = list(dict_result.keys())
    for item in key_values:
        bin = int(item/5)
        bin_name = str(5*bin) + '-' + str(5*bin+5)
        # print(a[item])
        dictionary_histogram[bin_name] += dict_result[item]
    print(dictionary_histogram) 
    return dictionary_histogram
##########################################
def EDA_education(df_user_skills):
    degree_level = ['degree','bachelors','masters','masters','phd','engineers','associate','researcher','Others']
    education_dictionary = {}
    for i in degree_level:
        education_dictionary[i] = 0

    for i in range (len(df_user_skills)):
        skills_list = df_user_skills.iloc[i]['user_vector']
        check = 0
        if len(skills_list) < 1 :
            continue
        else:
            for item in degree_level:
                if item in skills_list:
                    check = 1
                    education_dictionary[item] +=1
        if check == 0:
            education_dictionary['Others'] += 1
    return education_dictionary




def valid_string_in_item(invalid_items:list,string_input=''):
    result = 0
    for item in invalid_items:
        if item in string_input:
            result = 1
            return result
    return result

def filter_advanced_level(skills_list:list):
    # total_list = []
    # for i in range(0,len(df)):
        # check_list = df.iloc[i]['skills'].copy()
    drop_list = []
    check_list = skills_list.copy()
    invalid_string = ['pregnancy','status','gender','vacation','people','sex','salary','month','health','insurance',
                            'email','inmai','holiday','qualification','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    valid_string_list = ['english','japanese','vietnamese','foreign language','data visualization','programming language','docker',
                            'python','sql','nosql','scrum','agile','data science',' r ','software','javascript','java','scala','data engineer','data scientist',
                            'business analysis','business analyst','data analysis','data analyst','statistic','big data','data lake','data warehouse','aws','gcp',
                            'data governance','data analysis','tensorflow','bi tools','power bi','nifi','etl','linux','unix','windows','postgresql','mysql','batch','real time',
                            'data pipeline','software engineer','software engineering','data engineering','data mining']

    for item in skills_list:
        if ('degree' in item) and (len(item)>len('degree')):
            s = item.replace('degrees','').replace('degree','').strip()
            s2 = item.split(' ')
            check_list.append('degree')
            check_list.append(s)
            check_list = check_list + s2
            check_list.remove(item)
        else:
            if valid_string_in_item(invalid_items=invalid_string,string_input = item) == 1:
                check_list.remove(item)

    check_list = list(set(check_list))
    check_list_2 = check_list.copy()

    for item in check_list:
        if item.count(" ")>=3:
                # print(item)
            for valid_item in valid_string_list:
                if valid_item in item:
                    check_list_2.append(valid_item)
            check_list_2.remove(item)
                # print(item)
            continue
            
                # print(item)
            # if 
        # print("LENGTH AFTER: ",len(check_list)) 
    # total_list.append(list(set(check_list_2)))
    check_list_2 = list(set(check_list_2))
    return check_list_2

import sys
sys.path.append('../')
from models.lstm_predict import predict
def get_skills(text=''):
    a = predict(text)
    result = filter_advanced_level(a)
    return result





def main():
    df_job = load_job_data()
    df_user = load_user_data()
    # df_result = recommend(df_user.iloc[56]['experience'],df_user.iloc[56]['user_vector'],df_job)
    # print(df_result)

# main()