import os
import json

def write_to_file(file, obj):
    """ Write the obj as json to file.
    It will overwrite the file if it exist
    It will create the folder if it doesn't exist.
    Args:
        file: the file's path, like : ./tmp/INFOX/repo_info.json
        obj: the instance to be written into file (can be list, dict)
    Return:
        none
    """
    path = os.path.dirname(file)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(file, 'w') as write_file:
        write_file.write(json.dumps(obj))
    print ('finish write %s to file....' % file)

def get_repo_info(main_path):
    """ Get the info of repo.
    Args:
        main_path: the file store location.
    Return:
        A json object.
    """
    with open(main_path + '/repo_info.json') as read_file:
        repo_info = json.load(read_file)
    return repo_info

def get_forks_info_dict(main_path):
    """ Get the info of fork.
    It includes language, description, forks number.

    Args:
        main_path: the file store location.
    Return:
        A dict contains information of the forks.
        The key is fork's full name, the value is a dict of fork's information.
    """
    # print '---------------------------------------'
    forks_info = {}
    with open(main_path + '/forks.json') as read_file:
        forks_list = json.load(read_file)
        for fork in forks_list:
            fork_name = fork["full_name"].split('/')[0]
            forks_info[fork_name] = fork
    return forks_info

"""
def get_forks_list(main_path):
    # Get the list of forks and it's last committed time.
    #Args:
    #    main_path: the file store location.
    #Return:
    #    A list of tuple of fork's full name and last committed time.
    
    forks = []
    dir_list = os.listdir(main_path)
    for dir in dir_list:
        if os.path.isdir(main_path + '/' + dir):
            with open(main_path + '/' + dir + '/commits.json') as read_file:
                commits = json.load(read_file)
                try:
                    date = commits[0]["commit"]["committer"]["date"]
                    forks.append((dir, date))
                except:
                    pass
                    # print "missing commit on %s" % dir
    return forks
"""
