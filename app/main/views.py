from flask import (render_template, redirect, url_for, current_app,
                   abort, flash, request, make_response)
from flask_login import login_required, current_user

from . import main
from .forms import *
from ..models import *

from ..analyse import analyser
from ..analyse import fork_comparer
from ..decorators import admin_required, permission_required


def db_find_project(project_name):
    return Project.objects(project_name=project_name).first()


def db_approximate_find_project_project_name(project_name):
    _exact_project = db_find_project(project_name)
    if _exact_project:
        return _exact_project
    else:
        return Project.objects(project_name__endswith=project_name).first()


def db_delete_project(project_name):
    Project(project_name=project_name).delete()
    ProjectFork(project_name=project_name).delete()
    ChangedFile(project_name=project_name).delete()


@main.route('/', methods=['GET', 'POST'])
def start():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return redirect(url_for('main.welcome'))


@main.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')


@main.route('/discover', methods=['GET', 'POST'])
def discover():
    form = SearchProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data.replace('/', '_')
        _find_result = db_approximate_find_project_project_name(
            _input_project_name)
        if _find_result:
            return redirect(url_for('main.project_overview', project_name=_find_result.project_name))
        else:
            flash('The Project (%s) is not be added. You can turn to Add to add it!' %
                  _input_project_name)
            return redirect(url_for('main.discover'))

    if current_user.is_authenticated:
        project_list = Project.objects(
            project_name__nin=current_user.followed_projects)
    else:
        project_list = Project.objects
    page = request.args.get('page', 1, type=int)  # default is 1st page
    pagination = project_list.order_by(
        '-fork_number').paginate(page=page, per_page=current_app.config['SHOW_NUMBER_FOR_PAGE'])
    projects = pagination.items
    return render_template('discover.html', form=form, projects=projects, pagination=pagination)


@main.route('/index', methods=['GET', 'POST'])
def index():
    project_list = Project.objects(
        project_name__in=current_user.followed_projects)
    page = request.args.get('page', 1, type=int)  # default is 1st page
    pagination = project_list.order_by(
        '-fork_number').paginate(page=page, per_page=current_app.config['SHOW_NUMBER_FOR_PAGE'])
    projects = pagination.items
    return render_template('index.html', projects=projects, pagination=pagination)


@main.route('/project_refresh/<project_name>', methods=['GET', 'POST'])
@login_required
@admin_required
def project_refresh(project_name):
    if not db_find_project(project_name):
        abort(404)
    analyser.start(project_name)
    return redirect(url_for('main.project_overview', project_name=project_name))


"""
@main.route('/fork_refresh/<fork_name>', methods=['GET', 'POST'])
@login_required
@admin_required
def fork_refresh(fork_name):
    pass
"""


@main.route('/project/<project_name>', methods=['GET', 'POST'])
def project_overview(project_name):
    """ Overview of the project
    :param project_name
    """
    if not db_find_project(project_name):
        abort(404)

    _contain_key_word = request.args.get("key_words")

    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.project_overview', project_name=project_name, key_words=search_form.content.data))

    _project = Project.objects(project_name=project_name).first()
    if _project.analyser_progress and _project.analyser_progress != "100%":
        flash('The Project (%s) is updating!' % project_name)

    _all_changed_files = {}
    _changed_files = ChangedFile.objects(project_name=project_name)
    for file in _changed_files:
        _all_changed_files[(file.fork_name, file.file_name)] = file
        
    _marked_files = set()
    pagination = None
    if _contain_key_word:

        _forks = ProjectFork.objects(project_name=project_name, key_words_by_tdidf=_contain_key_word, file_list__ne=[]).order_by('-last_committed_time')
        if not _forks:
            _forks = ProjectFork.objects(project_name=project_name, key_words_by_tfidf=_contain_key_word, file_list__ne=[]).order_by('-last_committed_time')
            if not _forks: 
                _forks = ProjectFork.objects(project_name=project_name, key_words=_contain_key_word, file_list__ne=[]).order_by('-last_committed_time')
        
        _contain_key_words_changed_files = ChangedFile.objects(
            project_name=project_name, key_words=_contain_key_word)
        for file in _contain_key_words_changed_files:
            _marked_files.add((file.fork_name, file.file_name))
        _show_forks = _forks
    else:
        _forks = ProjectFork.objects(project_name=project_name, file_list__ne=[], key_words__ne=[]).order_by('-last_committed_time')
        page = request.args.get('page', 1, type=int) # default is 1st page
        pagination = _forks.paginate(page=page, per_page=current_app.config['SHOW_NUMBER_FOR_FORKS'])
        _show_forks = pagination.items

    _active_fork_number = _forks.count()
    return render_template('project_overview.html', project=_project, forks=_show_forks, key_word=_contain_key_word,
                           active_fork_number=_active_fork_number, search_form=search_form,
                           all_changed_files=_all_changed_files, marked_files=_marked_files, pagination=pagination)


def db_add_project(project_name):
    _project_name = project_name.replace('/', '_')
    if not db_find_project(_project_name):
        analyser.start(_project_name)
        return True
    else:
        return False

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddProjectForm()
    if form.validate_on_submit():
        _input = form.project_name.data
        if db_add_project(_input):
            flash('The Project (%s) is added. The data is loading......' % _input)
            return redirect(url_for('main.index'))
        else:
            flash('The Project (%s) has already added!' % _input)
            return redirect(url_for('main.add'))
    return render_template('add.html', form=form)


"""
@main.route('/localadd', methods=['GET', 'POST'])
@login_required
@admin_required
def localadd():
    form = AddProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        analyser.analyse_project(_input_project_name, False)
        return redirect(url_for('main.project_overview', project_name=_input_project_name))
    return render_template('localadd.html', form=form)
"""

"""
@main.route('/load_from_github',methods=['GET', 'POST'])
@login_required
def load_from_github():
    pass
"""


@main.route('/delete', methods=['GET', 'POST'])
@login_required
@admin_required
def delete():
    form = DeleteProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        if db_find_project(_input_project_name):
            db_delete_project(_input_project_name)
            flash('The project (%s) is already deleted!' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            flash('The project (%s) is not found.' % _input_project_name)
            return redirect(url_for('main.delete'))
    return render_template('delete.html', form=form)

def db_followed_project(project_name):
    if db_find_project(project_name):
        User.objects(username=current_user.username).update_one(push__followed_projects=project_name)
        return True
    else:
        return False

@main.route('/followed_project/<project_name>', methods=['GET', 'POST'])
@login_required
def followed_project(project_name):
    if db_followed_project(project_name):
        flash('Followed Project %s successfully!' % project_name) 
    else:
        flash('Project not found!')
    return redirect(url_for('main.project_overview', project_name=project_name))

@main.route('/unfollowed_project/<project_name>', methods=['GET', 'POST'])
@login_required
def unfollowed_project(project_name):
    User.objects(username=current_user.username).update_one(
        pull__followed_projects=project_name)
    return redirect(url_for('main.index'))


"""
@main.route('/followed_fork/<fork_name>', methods=['GET', 'POST'])
@login_required
def followed_fork(fork_name):
    _fork = ProjectFork.objects(fork_name = fork_name).first() # guarteen the fork name unique
    if _fork:
        current_user.update_one(push__followed_forks=fork_name)
        current_user.update_one(push__followed_projects=_fork.project_name)
        return redirect(url_for('main.project_overview', project_name=_fork.project_name))
    else:
        flash('Fork not found!')
    return redirect(url_for('main.index'))

@main.route('/unfollowed_fork/<fork_name>', methods=['GET', 'POST'])
@login_required
def unfollowed_fork(fork_name):
    current_user.update_one(pull__followed_forks=fork_name)
    return redirect(url_for('main.index'))
"""


@main.route('/compare_fork', methods=['GET', 'POST'])
def compare_fork():
    """ Compare two forks by Key words
    """
    form = CompareForkForm()
    if form.validate_on_submit():
        return redirect(url_for('main.compare_fork', form=form, fork1=form.fork1.data, fork2=form.fork2.data))

    _fork1_name = request.args.get("fork1")
    _fork2_name = request.args.get("fork2")
    if _fork1_name and _fork2_name:
        _fork1 = ProjectFork.objects(fork_name=_fork1_name).first()
        _fork2 = ProjectFork.objects(fork_name=_fork2_name).first()
        if _fork1 and _fork2:
            _common_files = fork_comparer.compare_on_files(_fork1, _fork2)
            _common_words = fork_comparer.compare_on_key_words(_fork1, _fork2)
            return render_template('compare_fork.html', form=form, common_files=_common_files, common_words=_common_words)
        else:
            if _fork1 is None:
                flash('(%s) is not found!' % form.fork1.data)
            if _fork2 is None:
                flash('(%s) is not found!' % form.fork2.data)
            return redirect(url_for('main.compare_fork'))
    return render_template('compare_fork.html', form=form)


@main.route('/about')
def about():
    """About Page
    """
    form = FeedbackForm()
    if form.validate_on_submit():
        flash('Feedback received successfully!')
        print(form.feedback.data)
        return redirect(url_for('main.about'))
    return render_template('about.html', form=form)


@main.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flask.flash('Logged in successfully.')
