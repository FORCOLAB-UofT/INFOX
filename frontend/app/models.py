from . import db

class ChangedFile(db.Document):
    project_name        = db.StringField(required=True)
    fork_name           = db.StringField(required=True)
    file_full_name      = db.StringField(required=True)
    file_language       = db.StringField(required=True)
    file_suffix         = db.StringField(required=True)
    changed_line_number = db.IntField()
    changed_code_number = db.StringField()
    key_words           = db.ListField(db.StringField())
    variable            = db.ListField(db.StringField())
    class_name          = db.ListField(db.StringField())
    function_name       = db.ListField(db.StringField())

class ProjectFork(db.Document):
    project_name                = db.StringField(required=True)
    fork_name                   = db.StringField(required=True, unique = True)
    last_committed_time         = db.DateTimeField()
    total_changed_line_number   = db.IntField()
    total_changed_file_number   = db.IntField()

class Project(db.Document):
	project_name 		= db.StringField(required=True, primary_key = True)
	language 			= db.StringField(default = "c++")
	fork_number 		= db.IntField(default = -1)
	feature_number 		= db.IntField(default = -1)
    # finish_crawlered    = db.BooleanField(default = False)
    
