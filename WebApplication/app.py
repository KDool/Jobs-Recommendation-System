from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect
from matplotlib.pyplot import bar_label
import yaml
import sys
sys.path.append('../')
import MatchingModule.recommend as recommend


app = Flask(__name__,template_folder='template')


@app.route('/')
def index():
    # return redirect('/user')
    return render_template('index.html')

@app.route('/input-user-recommend',methods=['GET', 'POST'])
def users():
    exp_list = []
    skills_list = []

    if request.method == 'POST':
        # Fetch form data
        experience = request.form['experience']
        skills = request.form['skills']
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
    print("DF RESULT: \n",df_result)
    # df_result = df_job_data[['job_id','jobTitle']]
    # Recommend from Skills/Experience
    return render_template('input_user.html', tables=[df_result.to_html(render_links=True, escape=False)], titles=[''])




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
        return render_template('choose-user.html',tables=[df_result.to_html(render_links=True, escape=False)], titles=[''])
    else:
        return render_template('choose-user.html')

# @app.route('')

if __name__ == '__main__':
    df_job_data = recommend.load_job_data()
    df_user_data = recommend.load_user_data()
    app.run(debug=True)

