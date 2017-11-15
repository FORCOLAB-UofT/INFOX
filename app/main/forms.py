from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField,
                     BooleanField, SelectField, ValidationError)
from wtforms.validators import Length


class AddProjectForm(FlaskForm):
    project_name = StringField(
        'Input the full name of the project (author_repo or author/repo)')
    submit = SubmitField('Add')


class DeleteProjectForm(FlaskForm):
    project_name = StringField(
        'Input the full name of the project (author_repo)')
    submit = SubmitField('Delete')


class SearchProjectForm(FlaskForm):
    project_name = StringField('Project Name')
    submit = SubmitField('Search')


class SearchForm(FlaskForm):
    content = StringField('Key Word')
    submit = SubmitField('Search')


class CompareForkForm(FlaskForm):
    fork1 = StringField('Fork1')
    fork2 = StringField('Fork2')
    submit = SubmitField('Compare')


class FollowedButton():
    submit = SubmitField('Followed')


class UnFollowedButton():
    submit = SubmitField('UnFollowed')
