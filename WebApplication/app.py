from cgi import test
from logging.handlers import RotatingFileHandler
from unittest import result
from flask import Flask, render_template, request, redirect
from graphviz import render
from matplotlib.pyplot import bar_label
import yaml
import sys
sys.path.append('../')
import MatchingModule.recommend as recommend
import pandas as pd

app = Flask(__name__,template_folder='template')


@app.route('/')
def index():
    # return redirect('/user')
    return render_template('home.html')


@app.route('/input-user-recommend',methods=['GET', 'POST'])
def users():
    exp_list = []
    skills_list = []

    if request.method == 'POST':
        # Fetch form data
        experience = request.form['userExp']
        skills = request.form['userSkills']
        print("EXP: ",experience)
        print("SKILLS: ",skills)
        exp_list = experience.split(',')

        for i in range(len(exp_list)):
            exp_list[i] = exp_list[i].strip()
        skills_list = skills.replace('\'','').split(',')
        for i in range(len(skills_list)):
            skills_list[i] = skills_list[i].strip()

        df_result = recommend.recommend(exp_list,skills_list,df_job_data)
        links = []
        for i in range(len(df_result)):
            job_link = 'https://www.linkedin.com/jobs/view/' + str(df_result.iloc[i]['job_id'])
            links.append(job_link)
        df_result['Link'] = links
        df_result = df_result[['job_id','jobTitle','Link','skills_match','similarity']]
        df_result = recommend.filter_threshold(df_result)
        df_result.rename(columns = {'similarity':'Score'}, inplace = True)
        print("DF RESULT: \n",df_result)
        # df_result = df_job_data[['job_id','jobTitle']]
        # Recommend from Skills/Experience
        return render_template('input_user.html', tables=[df_result.to_html(render_links=True, escape=False)], titles=[''])
    else:
        return render_template('input_user.html')



@app.route('/EDA-job-barchart')
def EDA_job_barchart():
    # df_DE = df_job_data[df_job_data["jobTitle"].str.contains("Data Engineer")]
    # df_job_skills = 
    bar_labels, bar_values = recommend.EDA_tile(df_job_data,'Data Engineer')
    return render_template('bar_chart.html',title='Most Frequent Skills', max=50, labels=bar_labels, values=bar_values)


@app.route('/EDA-user-barchart',methods=['GET', 'POST'])
def EDA_user_barchart():
    # df_DE = df_job_data[df_job_data["jobTitle"].str.contains("Data Engineer")]
    # df_job_skills = 
    if request.method == 'POST':
        id = request.form["roleTitle"]
        bar_labels, bar_values = recommend.EDA_user_role(df_user_data,id)
        return render_template('bar_chart.html',title='Most Frequent Skills for '+id , max=500,labels=bar_labels, values=bar_values)
    else:
        return render_template('bar_chart.html')



@app.route('/search',methods=['GET', 'POST'])
def search_userId():
    if request.method == 'POST':
        id = request.form["userID"]
        print("DATA: ",id)
        user = df_user_data[df_user_data['_id']==id].iloc[0]
        df_result = recommend.recommend(user['experience'],user['user_vector'],df_job_data)

        links = []
        for i in range(len(df_result)):
            job_link = 'https://www.linkedin.com/jobs/view/' + str(df_result.iloc[i]['job_id'])
            links.append(job_link)
        df_result['Link'] = links
        df_result = df_result[['job_id','jobTitle','Link','skills_match','similarity']]
        df_result = recommend.filter_threshold(df_result)
        df_result.rename(columns = {'similarity':'Score'}, inplace = True)

        return render_template('choose-user.html',tables=[df_result.to_html(render_links=True, escape=False)], titles=[''])
    else:
        return render_template('choose-user.html')


@app.route('/compare-user',methods=['GET', 'POST'])
def compare_user():
    if request.method == 'POST':
        user1_id = request.form['user1_id']
        user2_id = request.form['user2_id']
        user1 = df_user_data[df_user_data['_id'] == user1_id].iloc[0].to_dict()
        user2 = df_user_data[df_user_data['_id'] == user2_id].iloc[0].to_dict()
        # user1 = {'experience':user1_exp,'user_vector':user1_skills}
        # user2 = {'experience':user2_exp,'user_vector':user2_skills}
        print(user1)
        print(user2)

        job_id = request.form['job_id']
        test_job = df_job_data[df_job_data['job_id']==int(job_id)].iloc[0]
        job_link = 'https://www.linkedin.com/jobs/view/' + str(test_job['job_id'])
        print(test_job)
        s1,m1,s2,m2 = recommend.compare_users_1JD(user1_vector=user1,user2_vector=user2,job_title=test_job['jobTitle'],job_vector=test_job['skills'])


        dictionary_result = [{'user_id':user1['_id'],'match skills':m1,'experience':user1['experience'],'score':s1,'Job Link':job_link,'Job Title':test_job['jobTitle']},
        {'user_id':user2['_id'],'match skills':m2,'experience':user2['experience'],'score':s2,'Job Link':job_link,'Job Title':test_job['jobTitle']},
        ]
        df_out = pd.DataFrame(dictionary_result)
        return render_template('compare-user.html',tables=[df_out.to_html(render_links=True, escape=False)], titles=[''])
        # return render_template('compare-user.html')
    else:
        return render_template('compare-user.html')

@app.route('/EDA-location')
def eda_location():
    bar_keys,bar_values = recommend.EDA_on_location(df_jobs)
    print(bar_keys,bar_values)
    return render_template('eda_location.html',title='EDA Jobs Locations', max=1500,labels=bar_keys, values=bar_values)

@app.route('/EDA-workingtypes')
def eda_workingtypes():
    bar_keys,bar_values = recommend.EDA_on_working(df_jobs)
    return render_template('eda_workingtypes.html',title='EDA Jobs Working Types', max=1500,labels=bar_keys, values=bar_values)


@app.route('/EDA-year-exp')
def eda_year_exp():
    result_dictionary = recommend.EDA_workingexp(df_user)
    print(result_dictionary)
    bar_keys = list(result_dictionary.keys())
    bar_values = list(result_dictionary.values())
    return render_template('eda_experience.html',title='EDA Users Experience By Year', max=2000,labels=bar_keys, values=bar_values)



@app.route('/EDA-user-education')
def eda_user_education():
    result_dictionary = recommend.EDA_education(df_user_data)
    print(result_dictionary)
    bar_keys = list(result_dictionary.keys())
    bar_values = list(result_dictionary.values())
    return render_template('eda_experience.html',title='EDA Users Education Level', max=5000,labels=bar_keys, values=bar_values)








if __name__ == '__main__':
    df_job_data = recommend.load_job_data()
    df_user_data = recommend.load_user_data()
    df_jobs = recommend.load_full_JDs()
    df_user = recommend.load_full_Users()
    # print("DF JOB: ",df_job_data)
    # print("DF USER: ",df_user_data)
    app.run(host='0.0.0.0', port=8080,debug=True)

