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
