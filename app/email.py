from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from . import mail


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


class EmailSender:
    def __init__(self, username, email_address, subject, template):
        self.username = username
        self.email_address = email_address
        self.subject = subject
        self.template = template

    def repo_finish(self, repo_list):
        if (self.email_address is not None) and (repo_list is not None):
            send_mail(self.email_address, self.subject, self.template, username=self.username, repo_list=repo_list)
