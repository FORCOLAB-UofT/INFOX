from flask import current_app
from flask_github import GitHub
from threading import Thread
from . import project_updater

current_analysing = set()

def start_analyse(app, project_name, analyse_github):
    if project_name in current_analysing:
        return

    print("-----start analysing for %s-----" % project_name)
    current_analysing.add(project_name)

    with app.app_context():
        repo_info = analyse_github.get('repos/%s' % project_name)
        print('finish fetch repo info for %s' % project_name)
        repo_forks_list = analyse_github.request('GET', 'repos/%s/forks' % project_name, True)
        print('finish fetch fork list for %s' % project_name)
        project_updater.start_update(project_name, repo_info, repo_forks_list)

    current_analysing.remove(project_name)
    print("-----finish analysing for %s-----" % project_name)


def start(project_name, analyser_access_token):
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

    Thread(target=start_analyse, args=[app, project_name, analyse_github]).start()
    return True

