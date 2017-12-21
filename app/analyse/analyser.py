import time

from flask import current_app
from flask_github import GitHub
from threading import Thread
from . import project_updater

current_analysing = set()

def start_analyse(app, project_name, analyse_github, email_sender):
    if project_name in current_analysing:
        return

    print("-----start analysing for %s-----" % project_name)
    current_analysing.add(project_name)

    with app.app_context():
        for try_time in range(5):
            try:
                print('try fetch repo info for %s' % project_name)
                repo_info = analyse_github.get('repos/%s' % project_name)
                print('finish fetch repo info for %s' % project_name)
                break
            except:
                time.sleep(10 * 60) # 10 mins

        
        
        project_updater.project_init(project_name, repo_info) # First updata for quick view.

        for try_time in range(5):
            try:
                print('try fetch fork list for %s' % project_name)
                repo_forks_list = analyse_github.request('GET', 'repos/%s/forks' % project_name, True)
                print('finish fetch fork list for %s' % project_name)
                break
            except:
                time.sleep(10 * 60) # 10 mins

        

        project_updater.start_update(project_name, repo_info, repo_forks_list)

        # Send email to user
        if (email_sender is not None) and (len(repo_forks_list) > 0):
            email_sender.repo_finish(project_name)

    current_analysing.remove(project_name)
    print("-----finish analysing for %s-----" % project_name)


def start(project_name, analyser_access_token, email_sender=None):
    app = current_app._get_current_object()

    analyse_github = GitHub(app)
    @analyse_github.access_token_getter
    def token_getter():
        # print("another place %s" % analyser_access_token)
        return analyser_access_token

    try:
        analyse_github.get('repos/%s' % project_name)
    except:
        return False

    Thread(target=start_analyse, args=[app, project_name, analyse_github, email_sender]).start()
    return True

