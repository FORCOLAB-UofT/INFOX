from flask import current_app
from threading import Thread

from . import api_crawler
from . import project_analyser

current_analysing = set()

def start_analyse(app, project_name):
    if project_name in current_analysing:
        return
    current_analysing.add(project_name)
    
    with app.app_context():
    	api_crawler.project_info_crawler(project_name)
    	project_analyser.analyse_project(project_name)

    current_analysing.remove(project_name)
    
def start(project_name):
    app = current_app._get_current_object()
    thread = Thread(target=start_analyse, args=[app, project_name])
    thread.start()
    return thread
