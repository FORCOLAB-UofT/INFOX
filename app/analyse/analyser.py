from flask import current_app
from flask_github import GitHub
from threading import Thread
from . import project_analyser

current_analysing = set()

def start_analyse(app, project_full_name, analyse_github):
    if project_full_name in current_analysing:
        return

    print("-----start analysing for %s-----" % project_full_name)
    current_analysing.add(project_full_name)

    with app.app_context():
        author, repo = project_full_name.split('_')
        repo_info = analyse_github.get('repos/%s/%s' % (author, repo))
        repo_forks_list = analyse_github.request('GET', 'repos/%s/%s/forks' % (author, repo), True)
        project_analyser.analyse_project(project_full_name, repo_info, repo_forks_list)

    current_analysing.remove(project_full_name)
    print("-----finish analysing for %s-----" % project_full_name)
    
def start(project_name, analyser_access_token):
    app = current_app._get_current_object()

    analyse_github = GitHub(app)
    @analyse_github.access_token_getter
    def token_getter():
        # print("another place %s" % analyser_access_token)
        return analyser_access_token

    Thread(target=start_analyse, args=[app, project_name, analyse_github]).start()
    #return thread
