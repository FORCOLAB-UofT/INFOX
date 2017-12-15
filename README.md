# INFOX

Website: http://forks-insight.com or http://128.2.112.151

Redesign for https://github.com/shuiblue/INFOX

How to run:
1. Ramp up the environment according to environment.yaml (you can load by anaconda)
2. Edit the config.py & env variable (see in config.py)
3. Run on localhost: python manage.py runserver

Language: Python3

Framework: Flask

Database: mongo



Code Overview:

./config.py

Config for Flask



./config.ini

Config for using uWSGI



./app/main

Entrance



./app/analyse

Crawler & Do analysis



./models

Database Model



./app/auth

Logic about account



./app/templates

HTML files



./app/static

CSS/Javascript/Img Resource



./app/email.py

Send email





