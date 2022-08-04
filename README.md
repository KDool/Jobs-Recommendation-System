# README
## Building data analytics and recommendation system for LinkedIn - Tutorial Document
Tutorial includes 3 sections
- Setup environments
- Traning Extract Skills Model with LSTM
- Deployment
- Features Usage

## Setup Environments
#### Environment requirements
- Operating System: 
    -- Crawler Servers: Windows 10, 
    -- Web server, MongoDB server: Ubuntu 18.04 LTS
- Python 3.9, pip3
- Docker engine

#### Install requirements
- **Linux Server**: 
    Install python 3.9, pip3:

        sudo apt-get install python3.9 
        sudo apt install python3-pip

    Install libraries/environments on Linux Server
        ```
        pip install -r -y requirements.txt
        ```
- **Windows Crawler Server**:
    Install Python 3.9, pip:
        -- Download and setup guide following this [link](https://www.python.org/downloads/)

    Install libraries/environments on windows server:
        ```
        pip install -r -y requirements_win.txt
        ```

##### MongoDB
On Linux Cloud server, run the following command: 
``` docker run -itd --name mongodb -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=admin mongo```

The username/password to access MongoDB is mongoadmin/admin
##### Windows Crawler
- Pull this repository and run the crawl.py

## Data Pre-processing
##### Clean and extract noun phrases from text.
Pull this repository on Linux machine and run the:  DataPreprocessing/build-NP-traning-dataset.ipynb

## Data Processing    
##### Traning Extract Skills Model with LSTM
- Download the dataset that I have labelled by myself from this [link](https://docs.google.com/spreadsheets/d/1PYIf_HrndDGP9x-XuZNcz6fwzuwv2oXfjbSQrKbWzvY/edit?usp=sharing), and save as CSV file at: output/total_phrases_labelled_train.csv
- Download pretrained dataset GloVe for English Word Representation from this [link](https://www.kaggle.com/datasets/rtatman/glove-global-vectors-for-word-representation)
- Training the model by running files: models/lstm.py
- Model evaluation: models/lstm.ipynb

##### Building user/job profiles
- User profiles: MatchingModule/users_vector.ipynb
- Job profiles: MatchingModule/jobs_vector.ipynb

## Data Analytics Engines
##### Recommendation Engine
- Recommendation engine is built at file MatchingModule/recommend.py
- Evaluate and Threshold analyzing at Evaluation/evaluate.ipynb
##### Exploratory Data Analytic Engine
- Recommendation engine is built at file MatchingModule/EDA.py


## Web Deployment
Website demo is built in the folder ./WebApplication
On Azure Cloud Server, in the repository directory, pull this repository and run the following commands:
```
cd WebApplication
python3 app.py
```
The homepage webserver will be available on http://mycloudserver-ip:8080. 



