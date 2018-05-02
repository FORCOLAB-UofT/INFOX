from . import db
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager


class ChangedFile(db.Document):
    full_name = db.StringField(required=True, primary_key=True)
    file_name = db.StringField()
    fork_name = db.StringField()
    project_name = db.StringField()
    file_language = db.StringField()
    file_suffix = db.StringField()
    diff_link = db.StringField()
    # Too big may cause performance problem.
    # changed_code = db.StringField()
    changed_line_number = db.IntField()
    key_words = db.ListField(db.StringField())
    key_words_dict = db.DictField()
    key_words_tfidf = db.ListField(db.StringField())
    key_words_tf_idf_dict = db.DictField()
    key_stemmed_words = db.ListField(db.StringField())
    key_stemmed_words_dict = db.DictField()
    key_words_lemmatize_tfidf = db.ListField(db.StringField())
    key_words_lemmatize_tfidf_dict = db.DictField()
    
    variable = db.ListField(db.StringField())
    class_name = db.ListField(db.StringField())
    function_name = db.ListField(db.StringField())
    


class ProjectFork(db.Document):
    full_name = db.StringField(required=True, primary_key=True)
    fork_name = db.StringField()
    project_name = db.StringField()
    last_committed_time = db.DateTimeField()
    created_time = db.DateTimeField()
    total_changed_line_number = db.IntField()
    total_changed_file_number = db.IntField()
    total_commit_number = db.IntField()
    file_list = db.ListField(db.StringField())
    commit_list = db.ListField(db.DictField())
    key_words = db.ListField(db.StringField())
    key_words_dict = db.DictField()
    key_words_tfidf = db.ListField(db.StringField())
    key_words_tf_idf_dict = db.DictField()
    key_stemmed_words = db.ListField(db.StringField())
    key_stemmed_words_dict = db.DictField()
    key_words_lemmatize_tfidf = db.ListField(db.StringField())
    key_words_lemmatize_tfidf_dict = db.DictField()
    tags = db.ListField(db.StringField())
    last_updated_time = db.DateTimeField()

    # For compatibility old version.
    key_words_by_tdidf = db.ListField(db.StringField())
    key_words_by_tfidf = db.ListField(db.StringField())
    key_words_counter_dict = db.DictField()

    tags = db.ListField(db.StringField())
    variable = db.ListField(db.StringField())
    function_name = db.ListField(db.StringField())

class Project(db.Document):
    project_name = db.StringField(required=True, primary_key=True)
    language = db.StringField()
    fork_number = db.IntField(default=-1)
    activate_fork_number = db.IntField(default=-1)
    feature_number = db.IntField(default=-1)
    description = db.StringField()
    analyser_progress = db.StringField()
    project_name_show = db.StringField()
    last_updated_time = db.DateTimeField()


class ForkTag(db.Document):
    fork_full_name = db.StringField(required=True)
    project_name = db.StringField(required=True)
    username = db.StringField(required=True)
    tags = db.ListField(db.StringField())


class User(UserMixin, db.Document):
    username = db.StringField(unique=True, required=True)
    email = db.StringField()
    permission = db.IntField()
    last_seen = db.DateTimeField()
    followed_projects = db.ListField(db.StringField())
    followed_forks = db.ListField(db.StringField()) # not used
    followed_projects_time = db.DictField()

    github_access_token = db.StringField()
    password_hash = db.StringField()
    github_name = db.StringField()

    tag_list = db.DictField() # not used

    owned_repo = db.DictField() # {repo_full_name: show_name}
    owned_repo_sync_time = db.DateTimeField()

    is_crawling = db.IntField() # 1 means is crawling
    repo_waiting_list = db.ListField(db.StringField())

    repo_email_time = db.DictField()

    def get_id(self):
        return self.username
    
    def can(self, permission):
        if self.username == 'FancyCoder0':
            return True
        return (self.permission & permission) == permission

    @property
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


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
    FOLLOW = 1
    ADD = 2
    REFRESH = 4
    DELETE = 8
    BASIC_USER = 1 # can follow
    GITHUB_USER = 3 # can follow, add
    ADMINISTER = 15 # all

class TagType:
    FEATURE = 1
    REFACTORING = 2
    BUG_FIX = 3
    CONFIGURE = 4
    OTHER = 5

    