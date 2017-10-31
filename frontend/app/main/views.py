# -*- coding: utf-8 -*-
from flask import (render_template, redirect, url_for, current_app,
                   abort, flash, request, make_response)

from . import main
from .forms import (AddProjectForm, SearchProjectForm)
from ..models import Project, ProjectFork

@main.route('/', methods=['GET', 'POST'])
def index():
    """ INFOX Homepage
    """
    form = SearchProjectForm()
    if form.validate_on_submit():
        # _user = User.query.filter_by(username=form.username.data).first()
        _input_project_name = form.project_name.data
        _find_project = Project.objects(project_name = _input_project_name).first()
        if _find_project is None:
            flash('The Project (%s) is not be added. You can turn to Add to add it!' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.project_overview', project_name = _input_project_name))

    page = request.args.get('page', 1, type=int) # default is 1st page
    pagination = Project.objects.paginate(page = page, per_page = 10)
    projects = pagination.items
    return render_template('index.html', form = form, projects = projects, pagination = pagination)


@main.route('/add', methods=['GET', 'POST'])
def add():
    """ Add Project
    """
    form = AddProjectForm()
    if form.validate_on_submit():
        _input_project_name = form.project_name.data
        # add project
        _find_project = Project.objects(project_name = _input_project_name).first()
        if _find_project is None:
            Project(project_name = _input_project_name).save()
            flash('The Project (%s) is added!' % _input_project_name)
            return redirect(url_for('main.index'))
        else:
            flash('The Project has already added!')
            return redirect(url_for('main.add'))
    return render_template('add.html', form=form)

@main.route('/project/<project_name>')
def project_overview(project_name): # add filter
    """ 查看指定用户信息

    :param project_name
    """
    _project = Project.objects(project_name = project_name).first()
    if _project is None:
        abort(404)

    """
    return render_template('project_overview.html',
                           project = _project,
                           forks = _project.forks)
    """

    page = request.args.get('page', 1, type=int) # default is 1st page
    pagination = ProjectFork.objects(project_name = project_name).paginate(page, per_page=10)
    forks = pagination.items
    return render_template('project_overview.html',
                           project = _project,
                           forks = forks,
                           pagination=pagination)

