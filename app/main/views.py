from flask import (render_template, redirect, url_for, current_app,
                   abort, flash, request, make_response)

from . import main
from .forms import *
from ..models import *

from ..analyse import analyser
from ..analyse import fork_comparer

def find_project(project_name):
    _find_project = Project.objects(project_name = project_name).first()
    if _find_project is None:
        return False
    else:
        return True

def delete_project(project_name):
    Project(project_name = project_name).delete()   
    ProjectFork(project_name = project_name).delete()
    ChangedFile(project_name = project_name).delete()
            
@main.route('/', methods=['GET', 'POST'])
def index():
    """ INFOX Homepage
    """
    form = SearchProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        if not find_project(_input_project_name):
            flash('The Project (%s) is not be added. You can turn to Add to add it!' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.project_overview', project_name=_input_project_name))

    page = request.args.get('page', 1, type=int) # default is 1st page
    pagination = Project.objects.order_by('-fork_number').paginate(page=page, per_page=current_app.config['SHOW_NUMBER_FOR_PAGE'])
    projects = pagination.items
    return render_template('index.html', form=form, projects=projects, pagination=pagination)

@main.route('/project_refresh/<project_name>', methods=['GET', 'POST'])
def project_refresh(project_name):
    if not find_project(project_name):
        abort(404)
    analyser.start(project_name)
    return redirect(url_for('main.project_overview', project_name=project_name))

@main.route('/project/<project_name>', methods=['GET', 'POST'])
def project_overview(project_name):
    """ Overview of the project
    :param project_name
    """
    if not find_project(project_name):
        abort(404)

    _contain_key_word = request.args.get("key_words")
    
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.project_overview', project_name=project_name, key_words=search_form.content.data))    

    _project = Project.objects(project_name = project_name).first()
    if _project.analyser_progress and _project.analyser_progress != "100%":
        flash('The Project (%s) is updating!' % project_name)

    # TODO fixed repeated code.
    _all_changed_files = {}
    _changed_files = ChangedFile.objects(project_name = project_name)
    for file in _changed_files:
        _all_changed_files[(file.fork_name, file.file_name)] = file.diff_link
    
    _marked_files = []
    if _contain_key_word:
        _forks = ProjectFork.objects(project_name = project_name, key_words = _contain_key_word, file_list__ne = []).order_by('-last_committed_time')
        _contain_key_words_changed_files = ChangedFile.objects(project_name = project_name, key_words = _contain_key_word)
        for file in _contain_key_words_changed_files:
            _marked_files.append((file.fork_name, file.file_name))
    else:
        _forks = ProjectFork.objects(project_name = project_name, file_list__ne = [], key_words__ne = []).order_by('-last_committed_time')
    
    return render_template('project_overview.html', project=_project, forks=_forks, search_form=search_form,
                           all_changed_files=_all_changed_files, marked_files = _marked_files)
    #page = request.args.get('page', 1, type=int) # default is 1st page
    #pagination = _forks.paginate(page=page, per_page=10)
    #forks = pagination.items
    
@main.route('/add', methods=['GET', 'POST'])
def add():
    """ Add Project
    """
    form = AddProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        _input_project_name = _input_project_name.replace('/','_')
        if not find_project(_input_project_name):
            analyser.start(_input_project_name)
            flash('The Project (%s) is added. The data is loading......' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            flash('The Project (%s) has already added!' % _input_project_name)
            return redirect(url_for('main.add'))
    return render_template('add.html', form=form)

"""
@main.route('/localadd', methods=['GET', 'POST'])
def localadd():
    form = AddProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        analyser.analyse_project(_input_project_name, False)
        return redirect(url_for('main.project_overview', project_name=_input_project_name))
    return render_template('localadd.html', form=form)
"""

@main.route('/delete', methods=['GET', 'POST'])
def delete():
    """ Delete Project
    """
    form = DeleteProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        if find_project(_input_project_name):
            delete_project(_input_project_name)
            flash('The project (%s) is already deleted!' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            flash('The project (%s) is not found.' % _input_project_name)
            return redirect(url_for('main.delete'))
    return render_template('delete.html', form=form)

@main.route('/compare_fork', methods=['GET', 'POST'])
def compare_fork():    
    """ Compare two forks by Key words
    """
    form = CompareForkForm()
    if form.validate_on_submit():
        return redirect(url_for('main.compare_fork', form=form, fork1 = form.fork1.data, fork2 = form.fork2.data)) 

    _fork1_name = request.args.get("fork1")
    _fork2_name = request.args.get("fork2")
    if _fork1_name and _fork2_name:
        _fork1 = ProjectFork.objects(fork_name = _fork1_name).first()
        _fork2 = ProjectFork.objects(fork_name = _fork2_name).first()
        if _fork1 and _fork2:
            _common_files = fork_comparer.compare_on_files(_fork1, _fork2)
            _common_words = fork_comparer.compare_on_key_words(_fork1, _fork2)
            return render_template('compare_fork.html', form=form, common_files = _common_files, common_words = _common_words)
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
    return render_template('about.html')

