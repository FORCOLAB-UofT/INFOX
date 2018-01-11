from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from . import mail
from .models import *

def send_async_email(app, msg):
    with app.app_context():  # make sure it works
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    """ use async to send email
    :param to
    :param subject
    :param template
    :param kwargs
    :return: thread
    """
    app = current_app._get_current_object()
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASK_MAIL_SENDER'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread

def send_mail_for_repo_finish(project_name):
    _user_list = User.objects(followed_projects=project_name)
    for user in _user_list:
        if user.email is not None:
            send_mail(user.email, 'Repo Status Update', 'email.html', project_name=project_name, username=user.username)


            