# -*- coding: utf-8 -*-
import os
import json

from ..models import ChangedFile, ProjectFork, Project

def load_data(path, project_name):
    forks_info = get_forks_info_dict(main_path)
    forks = get_forks_list(main_path)
    
    dir_list = os.list_dir(main_path)
    for dir in dir_list:
        if os.path.isdir(main_path + '/' + dir):
            
            with open(main_path + '/' + dir + '/result.json') as read_file:
                result = json.load(read_file)
                
                for file in result["file_list"]:
                    ChangedFile(
                        project_name = 
                        fork_name = 
                        file_full_name = file["file_full_name"]
                        # file_language
                        file_suffix = file["file_suffix"]
                        changed_line = file["changed_line"]
                        changed_code = file["changed_code"]
                        key_words = file["tokens"]
                        # variable 
                        # class_name 
                        # function_name 
                    ).save();
                
                ProjectForks(
                    project_name = 
                    fork_name = 
                    total_changed_file_number = result["changed_file_number"]
                    total_changed_line_number = result["changed_line"]
                    # last_committed_time
                ).save();
                
             