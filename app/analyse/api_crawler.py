"""
crawler.py is to get the information of the project and the forks of it from Github's API.
Now, the data is stored in LOCAL_DATA_PATH(set in config).
"""

import os
import json
import requests
from flask import current_app

from .util import localfile_tool

# commits_page_limit = 1 # 1 is just for checking the status, if you need more commits set it larger.
api_limit_error = 'API rate limit exceeded'

def get_api_with_params(url, params):
    try:
        response = requests.get(url, params=params)
        # if api_limit_error in response.text[:100]:
        #     raise api_limit_error
    except requests.RequestException as error:
        print(error)
    return response.json()

def get_api(url):
    return get_api_with_params(url, { 'access_token': current_app.config['ACCESS_TOKEN'] })

def page_iter(base_url):    
    page_num = 0
    result = []
    # Do the loop until getting the empty response.
    # last_json_result = None
    params = { 'access_token': current_app.config['ACCESS_TOKEN'] }
    while True:
        page_num += 1
        params['page'] = page_num
        json_result = get_api_with_params(base_url, params)
        #print(json_result)
        # If the response is empty, then break the loop.
        if not json_result:
            break
        # if json_result == last_json_result:
        #     break
        # last_json_result = json_result

        for item in json_result:
            result.append(item)

    print('finish crawling! Get all pages for %s!' % (base_url))
    return result

def get_user_starred_list(username):    
    raw_data = page_iter('https://api.github.com/users/%s/%s' % (username, 'starred'))
    starred_list=[]
    try:
        starred_list = [starred["full_name"] for starred in raw_data]
        if raw_data:
            localfile_tool.write_to_file(current_app.config['LOCAL_DATA_PATH'] + '/users_info/' + username + "/starred.json" , raw_data)
    except:
        raise 'Error on get_user_starred_list!'
    return starred_list

def get_repo(author, repo, type=""):
    """The general function to get the data using Github's API.
    There is two cases:
    when type is not empty, iterator for page is need which means the data is iterated(like get all the forks for the repo),
    this function will get all the items.
    Args:
        author: like FancyCoder0
        repo: like INFOX
        type: one of [forks, branches, commits]
        For example:
            get_repo('FancyCoder0', 'INFOX', "")
            get_repo('FancyCoder0', 'INFOX', "forks")
    Return:
        If the type is not set, return a json object for response.
        If the type is set, return a list of json objects for all the items.
    """
    if not type:
        return get_api('https://api.github.com/repos/%s/%s' % (author, repo))
    else:
        return page_iter('https://api.github.com/repos/%s/%s/%s' % (author, repo, type))

def project_info_crawler(project_full_name):
    author_name, project_name = project_full_name.split('_')
    save_path = current_app.config['LOCAL_DATA_PATH']
    main_pain = save_path + '/' + author_name + '_' + project_name

    print("-----start crawling for %s-----" % project_name)

    if current_app.config['ALLOW_FORKS_UPDATE'] or (not os.path.exists(main_pain + '/repo_info.json')) or (not os.path.exists(main_pain + '/forks.json')):
        repo_info = get_repo(author_name, project_name, '')
        localfile_tool.write_to_file(main_pain + '/repo_info.json', repo_info)

        forks_list = get_repo(author_name, project_name, 'forks')
        localfile_tool.write_to_file(main_pain + '/forks.json', forks_list)

    print("-----finish crawling for %s-----" % project_name)

    """
    # Get all forks' commits.
    for fork in forks_list:
        author, repo = fork["full_name"].split('/')
        commits_list = get_api(author, repo, "commits")
        localfile_tool.write_to_file(main_pain + '/' + author + '/commits.json', commits_list)
    """


"""
if __name__ == '__main__':
    project_info_crawler('shuiblue/INFOX')
"""
