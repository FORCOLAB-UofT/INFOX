import time

from flask import current_app
from flask_github import GitHub
import threading
from . import project_updater
from .. import email

current_analysing = set()
current_analysing_lock = threading.Lock()

def get_current_analysing():
    if current_analysing_lock.acquire():
        result = current_analysing.copy()
        current_analysing_lock.release()
    return result

def start_analyse(app, project_name, analyse_github):
    global current_analysing, current_analysing_lock

    if project_name in current_analysing:
        return

    print("-----start analysing for %s-----" % project_name)

    if current_analysing_lock.acquire():
        current_analysing.add(project_name)
        # print('current_analysing',current_analysing)
        current_analysing_lock.release()

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
        email.send_mail_for_repo_finish(project_name)

    if current_analysing_lock.acquire():
        current_analysing.remove(project_name)
        current_analysing_lock.release()

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

    threading.Thread(target=start_analyse, args=[app, project_name, analyse_github]).start()
    return True

