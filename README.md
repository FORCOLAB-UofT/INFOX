# INFOX

Website: http://forks-insight.com

Another related repo: https://github.com/shuiblue/INFOX



INFOX 



Language: Python3

Framework: Flask

Database: mongo

Http server: uwsgi & nginx



# How to run:

1. Ramp up the environment according to environment.yaml

   Here is an example of using Anaconda:

 - install conda (python3 version) [Download Anaconda](https://www.anaconda.com/download) 

 - install dependencies using [environment.yaml](https://github.com/FancyCoder0/INFOX/blob/master/environment.yaml)

   ``` bash
   conda env create -f environment.yaml
   ```


2. Install mongodb

   for mac user:

   ``` bash
   brew install mongodb
   ```

3. Edit the config (see in [config.py](https://github.com/FancyCoder0/INFOX/blob/master/config.py)) & Set the environment variables

   1. Check the config.py

   2. ``` bash
         export GITHUB_CLIENT_ID=[your_github_oAuth_Client_ID]

         export GITHUB_CLIENT_SECRET=[your_github_oAuth_Client_Secret]

         export INFOX_LOCAL_DATA_PATH=[local path for storing analyzed result (like /Users/fancycoder/infox_data)]

         export INFOX_SECRET_KEY=[a random string(like abcd1234)]

         export INFOX_MAIL_USERNAME=[smtp_username]

         export INFOX_MAIL_PASSWORD=[smtp_password]
         ```

4. Run on localhost: 

   If you using conda, start the virtual environment:

   ```bash
   source activate p3  (p3 is the env's name, see in environment.yaml)
   ```

   Then run it:

   ```bash
   python manage.py runserver
   ```

5. Run on Server:

   An example: [Serve Flask Applications with uWSGI and Nginx on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04)

   ​


Code Overview:

![code_architecture](./app/static/img/code_architecture.png)

./config.py - Config for Flask

./config.ini - Config for using uWSGI

./app/main - Program Entrance

./app/analyse - Crawler & Do analysis

./models - Database Model

./app/auth - Logic about account

./app/templates - HTML files

./app/static - CSS/Javascript/Img Resource

./manage.py - Start script used for testing

./wsgi - Start script for uwsgi

./celery_worker.py - Start script for crawler worker

