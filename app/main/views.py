from flask import g, jsonify, Markup, render_template, redirect, url_for, current_app, abort, flash, request, make_response
from flask_login import login_required, current_user
from datetime import datetime
from mongoengine.queryset.visitor import Q

from . import main
from .forms import *
from ..models import *

from ..analyse import analyser
from ..analyse import fork_comparer
from ..decorators import admin_required, permission_required

from ..auth.views import get_user_repo_list, get_upperstream_repo


#------------------------------------------------------------------
# Following are all the function wrap the database operation.
def db_find_project(project_name):
    return Project.objects(project_name=project_name).first()

def db_delete_project(project_name):
    Project.objects(project_name=project_name).delete()
    ProjectFork.objects(project_name=project_name).delete()
    ChangedFile.objects(project_name=project_name).delete()

def db_followed_project(project_name):
    if project_name not in current_user.followed_projects:
        User.objects(username=current_user.username).update_one(push__followed_projects=project_name)
    # Update project followed time
    tmp_dict = current_user.followed_projects_time
    tmp_dict[project_name] = datetime.utcnow()
    User.objects(username=current_user.username).update_one(set__followed_projects_time=tmp_dict)

def db_unfollowed_project(project_name):
    User.objects(username=current_user.username).update_one(
        pull__followed_projects=project_name)
    tmp_dict = current_user.followed_projects_time
    if project_name in tmp_dict:
        tmp_dict.pop(project_name)
    User.objects(username=current_user.username).update_one(set__followed_projects_time=tmp_dict)


#------------------------------------------------------------------
@main.route('/', methods=['GET', 'POST'])
def start():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return redirect(url_for('main.welcome'))


@main.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')


@main.route('/compare_forks', methods=['GET', 'POST'])
def compare_forks():
    """ Compare two forks by Key words
    """
    form = CompareForkForm()
    if form.validate_on_submit():
        return redirect(url_for('main.compare_forks', form=form, fork1=form.fork1.data, fork2=form.fork2.data))

    _fork1_name = request.args.get("fork1")
    _fork2_name = request.args.get("fork2")
    if _fork1_name and _fork2_name:
        _fork1 = ProjectFork.objects(fork_name=_fork1_name).first()
        _fork2 = ProjectFork.objects(fork_name=_fork2_name).first()
        if _fork1 and _fork2:
            _common_files = fork_comparer.compare_on_files(_fork1, _fork2)
            _common_words = fork_comparer.compare_on_key_words(_fork1, _fork2)
            return render_template('compare_forks.html', form=form, common_files=_common_files, common_words=_common_words)
        else:
            if _fork1 is None:
                flash('(%s) is not found!' % form.fork1.data, 'warning')
            if _fork2 is None:
                flash('(%s) is not found!' % form.fork2.data, 'warning')
            return redirect(url_for('main.compare_fork'))
    return render_template('compare_forks.html', form=form)


@main.route('/load_from_github', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD)
def load_from_github():
    if current_user.owned_repo_sync_time is not None:
        _ownered_project = list(current_user.owned_repo.items())
    else:
        return redirect(url_for('main.sync'))

    class ProjectSelection(FlaskForm):
        pass
    for project in _ownered_project:
        setattr(ProjectSelection, project[0], BooleanField(project[1], default=project[0] in current_user.followed_projects))
    setattr(ProjectSelection, 'load_button', SubmitField('Follow'))
    setattr(ProjectSelection, 'sync_button', SubmitField('Refresh List'))

    form = ProjectSelection()
    if form.load_button.data:
        at_least_one_load = False
        add_list = []
        for field in form:
            if field.type == "BooleanField" and field.data:
                at_least_one_load = True
                _project_name = field.id
                if not db_find_project(_project_name):
                    add_list.append(_project_name)
                db_followed_project(_project_name)
        analyser.add_repos(current_user.username, add_list)
        if at_least_one_load:
            flash('All the selected repos start loading into INFOX. We will send you emails to update status. Please wait.', 'info')
        return redirect(url_for('main.index'))
    elif form.sync_button.data:
        return redirect(url_for('main.sync'))

    return render_template('load_from_github.html', form=form)


@main.route('/sync', methods=['GET', 'POST'])
@login_required
def sync():
    """ Sync owned repos with GitHub
    """
    _ownered_project = []
    _tmp_project_list = get_user_repo_list(current_user.username)
    if _tmp_project_list:
        for project in _tmp_project_list:
            _ownered_project.append((project, project))
            # Add upperstream_repo
            upperstream_repo = get_upperstream_repo(project)
            if upperstream_repo is not None:
                _ownered_project.append((upperstream_repo, upperstream_repo + "(Upperstream of %s)" % project))

    User.objects(username=current_user.username).update_one(set__owned_repo_sync_time=datetime.utcnow())

    # mongoDB don't support key value contains '.'
    for i in range(len(_ownered_project)):
        _ownered_project[i] = (_ownered_project[i][0].replace('.', '[dot]'), _ownered_project[i][1])
    User.objects(username=current_user.username).update_one(set__owned_repo=dict(_ownered_project))

    flash('Refresh your own GitHub repositories list successfully!', 'success')
    return redirect(url_for('main.load_from_github'))

@main.route('/guide', methods=['GET', 'POST'])
@login_required
def guide():
    return render_template('guide.html')

@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # TODO:implement smart search.
    _search_form = SearchProjectForm()
    if _search_form.validate_on_submit():
        print(_search_form.project_name.data)
        return redirect(url_for('main.index', search=_search_form.project_name.data))
    
    _keyword_search = request.args.get('search')
    if _keyword_search:
        project_list = Project.objects(Q(project_name__in=current_user.followed_projects) & Q(project_name__contains=_keyword_search))
        if len(project_list) == 0:
            flash(Markup('Sorry, we don\'t find (%s) in your followed repositories. Try <a href="/find_repos" class="alert-link">Search on GitHub</a>.' % _keyword_search), 'warning')
            return redirect(url_for('main.index'))
    else:
        project_list = Project.objects(project_name__in=current_user.followed_projects)
        if len(project_list) == 0:
            return redirect(url_for('main.guide'))
    
    page = request.args.get('page', 1, type=int)  # default is 1st page
    pagination = project_list.paginate(page=page, per_page=current_app.config['SHOW_NUMBER_FOR_PAGE'])
    projects = pagination.items
    return render_template('index.html', projects=projects, pagination=pagination, time_now=datetime.utcnow(), form=_search_form)


@main.route('/project/<path:project_name>', methods=['GET', 'POST'])
def project_overview(project_name):
    """ Overview of the project
        Args:
            project_name
    """
    if not db_find_project(project_name):
        abort(404)

    _project = Project.objects(project_name=project_name).first()
    _forks = ProjectFork.objects(project_name=project_name, file_list__ne=[], total_changed_line_number__ne=0)
    

    # TODO _all_tags could be opted by AJAX
    _all_tags = {}
    if current_user.is_authenticated:
        _project_tags = ForkTag.objects(project_name=project_name, username=current_user.username)
        for tag in _project_tags:
            _all_tags[tag.fork_full_name] = tag.tags
    
    if current_user.is_authenticated:
        print('View: ', current_user.username, project_name)

    return render_template('project_overview.html', project=_project, forks=_forks, all_tags=_all_tags)


@main.route('/followed_project/<path:project_name>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def followed_project(project_name):
    db_followed_project(project_name)
    flash(Markup('Followed Project %s successfully! Please click <a href="/project/%s" class="alert-link">here</a> to view.' % (project_name, project_name)), 'success')
    return redirect(url_for('main.find_repos'))

@main.route('/unfollowed_project/<path:project_name>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.FOLLOW)
def unfollowed_project(project_name):
    db_unfollowed_project(project_name)
    return redirect(url_for('main.index'))

@main.route('/find_repos', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD)
def find_repos():
    form = AddProjectForm()
    if form.validate_on_submit():
        _input = form.project_name.data
        if db_find_project(_input) is not None:
            db_followed_project(_input)
            flash(Markup('The repo (%s) is already in INFOX. Followed successfully! Please click <a href="/project/%s" class="alert-link">here</a> to view.' % (_input, _input)), 'success')
        else:
            if analyser.check_repo(_input, current_user.github_access_token) is not None:
                analyser.add_repos(current_user.username, [_input])
                db_followed_project(_input)
                flash('The repo (%s) starts loading into INFOX. We will send you an email when it is finished. Please wait.' % _input, 'info')
            else:
                flash('Not found!', 'danger')

    if current_user.is_authenticated:
        project_list = Project.objects(
            project_name__nin=current_user.followed_projects)
    else:
        project_list = Project.objects

    page = request.args.get('page', 1, type=int)  # default is 1st page
    pagination = project_list.order_by('-fork_number').paginate(page=page, per_page=current_app.config['SHOW_NUMBER_FOR_PAGE'])
    projects = pagination.items
    return render_template('find_repos.html', form=form, projects=projects, pagination=pagination, time_now=datetime.utcnow())


@main.route('/about')
def about():
    """About Page
    """
    form = FeedbackForm()
    if form.validate_on_submit():
        flash('Feedback received successfully!', 'success')
        print(form.feedback.data)
        return redirect(url_for('main.about'))
    return render_template('about.html', form=form)

# ---------------- Following is all admin required. ----------------

@main.route('/admin_manage')
@login_required
@admin_required
def admin_manage():
    _projects = Project.objects()
    _users = User.objects()
    return render_template('admin_manage.html', projects=_projects, users=_users, time_now=datetime.utcnow())

@main.route('/project_refresh/<path:project_name>', methods=['GET', 'POST'])
@login_required
@admin_required
def project_refresh(project_name):
    """ Refresh the specfic project.
    """
    if not db_find_project(project_name):
        abort(404)
    analyser.add_repos(current_user.username, [project_name])
    return redirect(url_for('main.admin_manage'))

@main.route('/user_refresh', methods=['GET', 'POST'])
@login_required
@admin_required
def user_refresh():
    User.objects().update(is_crawling = 0)
    User.objects().update(repo_waiting_list = [])
    flash('Refresh all users successfully!', 'success')
    return redirect(url_for('main.admin_manage')) 

@main.route('/repo_refresh', methods=['GET', 'POST'])
@login_required
@admin_required
def project_refresh_all():
    """ Refresh all the project.
    """
    project_list = Project.objects()
    analyser.add_repos(current_user.username, [repo.project_name for repo in project_list])
    flash('Refresh all successfully!', 'success')
    return redirect(url_for('main.admin_manage'))

@main.route('/repo_refresh_for_unfinished', methods=['GET', 'POST'])
@login_required
@admin_required
def repo_refresh_for_unfinished():
    """ Refresh all the project which is unfinished.
    """
    project_list = Project.objects()
    crawl_list = []
    for repo in project_list:
        if repo.analyser_progress != "100%":
            crawl_list.append(repo.project_name)
    analyser.add_repos(current_user.username, crawl_list)
    flash('Refresh for unfinished successfully!', 'success')
    return redirect(url_for('main.admin_manage'))


@main.route('/delete_project/<path:project_name>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_project(project_name):
    db_delete_project(project_name)
    flash('The repo (%s) is deleted!' % project_name, 'success') 
    return redirect(url_for('main.admin_manage'))


@main.route('/delete_user/<username>')
@login_required
@admin_required
def delete_user(username):
    User.objects(username=username).delete()
    flash('User (%s) is deleted!' % username, 'success')
    return redirect(url_for('main.admin_manage'))


@main.route('/_fork_edit_tag', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD)
def _fork_edit_tag():
    _full_name = request.args.get('full_name')
    _tag = request.args.get('tag')
    _oper = request.args.get('oper')
    # print(current_user.username, _full_name, _tag, _oper)
    _user_fork_tag = ForkTag.objects(fork_full_name=_full_name, username=current_user.username).first()
    if _user_fork_tag is None:
        _fork = ProjectFork.objects(full_name=_full_name).first()
        if _fork is None:
            return None
        ForkTag(fork_full_name=_full_name, project_name=_fork.project_name, username=current_user.username).save()
        _user_fork_tag = ForkTag.objects(fork_full_name=_full_name, username=current_user.username).first()

    if _oper == 'delete':
        if _tag:
            ForkTag.objects(fork_full_name=_full_name, username=current_user.username).update_one(pull__tags=_tag)
    elif _oper == 'add':
        if _tag and (_tag not in _user_fork_tag.tags):
            ForkTag.objects(fork_full_name=_full_name, username=current_user.username).update_one(push__tags=_tag)
    elif _oper == 'clear':
        ForkTag.objects(fork_full_name=_full_name, username=current_user.username).update_one(set__tags=[])
    upd_tags = ForkTag.objects(fork_full_name=_full_name, username=current_user.username).first()
    return jsonify(",\n".join(upd_tags.tags))

@main.route('/_get_similar_fork', methods=['GET', 'POST'])
def _get_similar_fork():
    _full_name = request.args.get('full_name')
    if _full_name is not None:
        _fork = ProjectFork.objects(full_name=_full_name).first()
        if _fork is None:
            return None
        _fork_list = ProjectFork.objects(project_name=_fork.project_name)
        _result = fork_comparer.get_similar_fork(_fork_list, _fork)
        return jsonify(result=_result)
    else:
        return None


@main.route('/_get_predict_tag', methods=['GET', 'POST'])
def _get_predict_tag():
    _full_name = request.args.get('full_name')
    _tag_list = ["merge", "update", "fix", "add", "branch", "pull", "request", "version", "readme", "master", "change", "delete", "release", "remote", "track", "test", "remove", "patch", "configuration", "upstream", "support", "missing", "move", "conflict", "config"]
    _tag_value = dict([(x, 0.0) for x in _tag_list])
    if _full_name is None:
        return None

    _fork = ProjectFork.objects(full_name=_full_name).first()
    if _fork is None:
        return None

    for commit in _fork.commit_list:
        for tag in _tag_list:
            _tag_value[tag] += commit["title"].lower().count(tag) * 3 + commit["description"].lower().count(tag)

    _sorted_tag = [(x,y) for x, y in sorted(_tag_value.items(), key=lambda x: x[1], reverse=True)]
    _sorted_tag = [(x,y) for x, y in filter(lambda x: x[1] > 0, _sorted_tag)]
    return jsonify(result=_sorted_tag[:5])

@main.route('/_get_fork_commit_list', methods=['GET', 'POST'])
def _get_fork_commit_list():
    _full_name = request.args.get('full_name')
    if _full_name:
        _fork = ProjectFork.objects(full_name=_full_name).first()
        if _fork:
            return jsonify(_fork.commit_list)
    return None

@main.route('/_get_fork_changed_file_list', methods=['GET', 'POST'])
def _get_fork_changed_file_list():
    _full_name = request.args.get('full_name')
    if _full_name:
        _fork = ProjectFork.objects(full_name=_full_name).first()
        if _fork:
            # TODO(use fullname)
            # If use fork.file_list, the dir is not full.
            _changed_files = ChangedFile.objects(fork_name=_fork.fork_name)
            result_list = []
            for file in _changed_files:
                result_list.append({'link':file.diff_link, 'title':file.file_name})
            return jsonify(result_list)
    return None

@main.route('/_get_fork_tag', methods=['GET', 'POST'])
@login_required
def _get_fork_tag():
    _full_name = request.args.get('full_name')
    if _full_name:
        _fork_tag = ForkTag.objects(fork_full_name=_full_name, username=current_user.username).first()
        if _fork_tag is None:
            user_tags = []
        else:
            user_tags = _fork_tag.tags
        result = []
        default_tags = ['Configuration', 'New Feature', 'Bug fix', 'Refactoring']
        for tag in default_tags:
            if tag in user_tags:
                result.append({'name':tag,'status':True})
            else:
                result.append({'name':tag,'status':False})
        for tag in user_tags:
            if tag not in default_tags:
                result.append({'name':tag,'status':True})
        return jsonify(result)
    return None

@main.route('/graph/<category>/<path:project_name>', methods=['GET', 'POST'])
def graph(category, project_name):
    return render_template('graph.html', category=category, project_name=project_name)

@main.route('/_get_pie_graph_data', methods=['GET', 'POST'])
def _get_pie_graph_data():
    category = request.args.get('category')
    project_name = request.args.get('project_name')
    graph_classify = {
        'commit':[0, 1, 5, 9, 99],
        'LOC': [0, 9, 99, 999, 9999],
        'file': [0, 1, 3, 9, 99, 999],
    }
    if category not in graph_classify:
        return None
    
    _fork_list = ProjectFork.objects(project_name=project_name, total_changed_line_number__ne=0)
    bound = graph_classify[category]
    num = len(bound)
    tot = [0 for i in range(num + 1)]
    for fork in _fork_list:
        if fork.total_changed_line_number is None:
            continue
        if category == 'commit':
            t = fork.total_commit_number
            if (fork.total_changed_line_number > 0) and (t == 0): # commit Bug
                t = 250
        elif category == 'LOC':
            t = fork.total_changed_line_number
        elif category == 'file':
            t = fork.total_changed_file_number

        for i in range(num + 1):
            if i == num:
                tot[i] += 1
            elif t <= bound[i]:
                tot[i] += 1
                break
    result = []
    for i in range(num + 1):
        if i == 0:
            result.append({'type': '0', 'total': tot[i]})
        elif i == num:
            result.append({'type': str(bound[i - 1] + 1) + '+', 'total': tot[i]})
        else:
            result.append({'type': str(bound[i]) if bound[i - 1] + 1 == bound[i] else str(bound[i - 1] + 1) + '~' + str(bound[i]), 'total': tot[i]})
    return jsonify(result)



@main.route('/repo_list', methods=['GET', 'POST'])
def repo_list():
    _project = Project.objects(analyser_progress="100%").order_by('-fork_number')
    result = []
    for project in _project:
        _forks = ProjectFork.objects(project_name=project.project_name, file_list__ne=[], total_changed_line_number__ne=0)
        result.append([project.project_name, project.fork_number, project.activate_fork_number, _forks.count()])
    return render_template('repo_list.html', result=result)

@main.route('/privacy_policy', methods=['GET', 'POST'])
def privacy_policy():
    return render_template('privacy_policy.html')

@main.route('/_search_log', methods=['GET', 'POST'])
def _search_log():
    if current_user.is_authenticated:
        print('Search: ', current_user.username, request.args.get('repo'), request.args.get('col'), request.args.get('input'))
    return jsonify(None)

"""
# ----------------------------  use for test ------------------------

@main.route('/admin_email_update')
@login_required
@admin_required
def admin_email_update():
    _users = User.objects()
    for user in _users:
        db_update_email(user.username)
    return redirect(url_for('main.admin_manage'))

@main.route('/test', methods=['GET', 'POST'])
def test():
    from ..analyse.util import word_extractor
    fork_list = ProjectFork.objects()
    s = ""
    for fork in fork_list:
        for commit in fork.commit_list:
            s+=commit["title"] + "\n"
            s+=commit["description"] + "\n"
    return jsonify(word_extractor.get_top_words_from_text(s, 50))

@main.route('/test_send_email', methods=['GET', 'POST'])
def test_send_email():
    email_sender = EmailSender('Luyao Ren', '375833274@qq.com', 'Repo Status Update', 'email.html')
    email_sender.repo_finish('test_repo')
    return 'Finish Send!'

"""
