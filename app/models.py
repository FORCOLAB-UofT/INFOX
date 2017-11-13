from . import db

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
    fork_name                   = db.StringField()
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

    
