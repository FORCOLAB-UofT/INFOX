# -*- coding: utf-8 -*-
import os
import json

# from .models import ChangedFile, ProjectFork, Project

def load_data(path, project_name):
    main_path = path + '/' + project_name
    #forks_info = get_forks_info_dict(main_path)
    #forks = get_forks_list(main_path)
    dir_list = os.listdir(main_path)
    for dir in dir_list:
        if os.path.isdir(main_path + '/' + dir):
            project_name = project_name
            fork_author = dir
            # print project_name, fork_author
        
            with open(main_path + '/' + dir + '/result.json') as read_file:
                result = json.load(read_file)
                
                for file in result["file_list"]:
                    
                
                
    
if __name__ == '__main__':
    load_data("/Users/fancycoder/infox_data/result", "timscaffidi_ofxVideoRecorder")