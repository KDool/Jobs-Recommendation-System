# README
## LinkedIn Data Analytics and Recommendation System Tutorial Document
Tutorial includes 3 sections
- Installation Guide
- Deployment
- Features Usage

## Installation
#### Environment requirements
- Operating System: 
    -- Crawler Servers: Windows, 
    -- Other components: Linux 
- Python 3.9, pip
- Docker

#### Install requirements
- Linux Server: 
        ```
        pip install -r requirements_linux.txt
        ```
- Windows Crawler Server:
        ```
        pip install -r requirements_win.txt
        ```

## Deployment
#### MongoDB
On Linux Cloud server, run the following command: 
``` docker run -itd --name mongodb -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=admin mongo```
The username/password to access MongoDB is mongoadmin/admin
#### Windows Crawler
- Pull this repository and run the files.py

#### Data Processing
- Pull this repository on Linux machine and run the notebook.ipynb

#### Web Demonstration
On Cloud Server, in the repository directory, run the following commands:
```
cd WebApplication
python3 app.py
```
The homepage webserver will be available on http://mycloudserver-ip:8080



