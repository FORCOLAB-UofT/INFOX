from . import db
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager

class ChangedFile(db.Document):
    full_name           = db.StringField(required=True, primary_key=True)
    file_name           = db.StringField()
    fork_name           = db.StringField()
    project_name        = db.StringField()    
    file_language       = db.StringField()
    file_suffix         = db.StringField()
    diff_link           = db.StringField()
    changed_code        = db.StringField()
    changed_line_number = db.IntField()
    key_words           = db.ListField(db.StringField())
    key_stemmed_words   = db.ListField(db.StringField())
    variable            = db.ListField(db.StringField())
    class_name          = db.ListField(db.StringField())
    function_name       = db.ListField(db.StringField())

class ProjectFork(db.Document):
    full_name                   = db.StringField(required=True, primary_key=True)
    fork_name                   = db.StringField(unique = True)
    project_name                = db.StringField()
    last_committed_time         = db.DateTimeField()
    created_time                = db.DateTimeField()
    total_changed_line_number   = db.IntField()
    total_changed_file_number   = db.IntField()
    file_list                   = db.ListField(db.StringField())
    key_words                   = db.ListField(db.StringField())
    key_stemmed_words           = db.ListField(db.StringField())
    key_words_by_tfidf          = db.ListField(db.StringField())
    key_words_by_tdidf          = db.ListField(db.StringField())
    key_words_counter_dict      = db.DictField()
    key_words_tf_idf_dict       = db.DictField()

class Project(db.Document):
    project_name              = db.StringField(required=True, primary_key=True)
    language 			      = db.StringField()
    fork_number               = db.IntField(default=-1)
    feature_number            = db.IntField(default=-1)
    description               = db.StringField()
    analyser_progress         = db.StringField()

class User(UserMixin, db.Document):
    username = db.StringField(unique=True, required=True)
    email = db.StringField()
    password_hash = db.StringField()
    permission = db.IntField()
    last_seen = db.DateTimeField()
    followed_projects = db.ListField(db.StringField())
    followed_forks = db.ListField(db.StringField())

    def get_id(self):
        return self.username

    def can(self, permission):
        if self.username == 'admin':
            return True
        return (self.permission & permission) == permission
    
    @property
    def is_administrator(self):
        return self.permission == Permission.ADMINISTER

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    @property
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(username):
    # Flask-Login callback fucntion for load user
    return User.objects(username=username).first()

class Permission:
    """
    权限类，用于指定权限常量。当常量组合时可以构造不同身份权限。
    """
    FOLLOW = 1
    ADD = 2
    DELETE = 4
    REFRESH = 8
    NORMAL_USER = 7
    ADMINISTER = 15           # 管理网站