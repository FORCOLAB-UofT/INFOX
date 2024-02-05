from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField,
                     BooleanField, SelectField, ValidationError)
from wtforms.validators import Length


class AddProjectForm(FlaskForm):
    project_name = StringField(
        'Input the full name of the repository (author/repo)')
    submit = SubmitField('Search & Follow')


class DeleteProjectForm(FlaskForm):
    project_name = StringField(
        'Input the full name of the repository (author/repo)')
    submit = SubmitField('Delete')


class SearchProjectForm(FlaskForm):
    project_name = StringField('')
    submit = SubmitField('Search')


class CompareForkForm(FlaskForm):
    fork1 = StringField('Fork1')
    fork2 = StringField('Fork2')
    submit = SubmitField('Compare')

class FeedbackForm(FlaskForm):
    feedback = TextAreaField('')
    submit = SubmitField('Send to us')

class SyncButton(FlaskForm):
    submit = SubmitField('Sync with Github')