# INFOX

Website: http://forks-insight.com or http://128.2.112.151

Redesign for https://github.com/shuiblue/INFOX

INFOX 

Language: Python3

Framework: Flask

Database: mongo

Http server: uwsgi  (./config.ini - Config for using uWSGI)

Reverse Agent: nginx (/etc/init.d/nginx)

How to run:

1. Ramp up the environment according to environment.yaml (you can load by anaconda)

 - install conda (package manager)
    https://conda.io/docs/user-guide/install/download.html
    Download Anaconda

 - install dependencies (https://github.com/FancyCoder0/INFOX/blob/master/environment.yaml)
   conda env create -f environment.yaml

 - install mongo (install brew mongo)


2. Edit the config.py & env variable (see in config.py) 
   (https://github.com/FancyCoder0/INFOX/blob/master/config.py)
 
   source activate p3

   export GITHUB_CLIENT_ID= [your_github_oAuth_Client_ID]
   export GITHUB_CLIENT_SECRET= [your_github_oAuth_Client_Secret]
   export INFOX_LOCAL_DATA_PATH= [local path for storing analyzed result]
   export INFOX_SECRET_KEY=[random string]
   export INFOX_MAIL_USERNAME= [smtp_username]
   export INFOX_MAIL_PASSWORD= [smtp_password]    

3. Run on localhost: python manage.py runserver


Code Overview:

./config.py - Config for Flask

./config.ini - Config for using uWSGI

./app/main - Program Entrance

./app/analyse - Crawler & Do analysis

./models - Database Model

./app/auth - Logic about account

./app/templates - HTML files

./app/static - CSS/Javascript/Img Resource

./app/email.py - Send email
