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


base_url = 'https://api.github.com/repos/%s/%s'
base_url_with_page = 'https://api.github.com/repos/%s/%s/%s?page=%d'
api_limit_error = 'API rate limit exceeded'

def validate_access_token(access_token):
    return len(access_token) == 40

def get_api(author, repo, type="", access_token=""):
    """The general function to get the data using Github's API.
    There is two cases:
    when type is not empty, iterator for page is need which means the data is iterated(like get all the forks for the repo),
    this function will get all the items.
    Args:
        author: like FancyCoder0
        repo: like INFOX
        type: one of [forks, branches, commits]
        access_token: your personal access token for limit of Github's API.
        For example:
            get_api('FancyCoder0', 'INFOX', "")
            get_api('FancyCoder0', 'INFOX', "forks")
    Return:
        If the type is not set, return a json object for response.
        If the type is set, return a list of json objects for all the items.
    """

    if not type:
        try:
            url = base_url % (author, repo)
            if access_token:
                url = url + ('?access_token=%s' % access_token)
            response = requests.get(url)
            if api_limit_error in response.text:
                raise Exception(api_limit_error)
        except requests.RequestException as error:
            print(error)
        print ('finish crawling!')
        return response.json()

    page_num = 0
    result = []
    # Do the loop until getting the empty response.
    while True:
        page_num += 1

        # This is manual limit to speed up checking the status.
        # if type == "commits" and page_num > commits_page_limit:
        #     break

        # print('page_num = %d' % page_num)
        try:
            url = base_url_with_page % (author, repo, type, page_num)
            if access_token:
                url = url + ('&access_token=%s' % access_token)
            response = requests.get(url)
            if api_limit_error in response.text:
                raise Exception(api_limit_error)
        except requests.RequestException as error:
            print(error)

        json_result = response.json()

        # If the response is empty, then break the loop.
        if not json_result:
            break

        for item in json_result:
            result.append(item)

    print ('finish crawling! Get all the %s !' % (type))
    return result

def project_info_crawler(project_full_name):
    author_name, project_name = project_full_name.split('_')
    save_path = current_app.config['LOCAL_DATA_PATH']
    access_token = current_app.config['ACCESS_TOKEN']
    if not validate_access_token(access_token):
        access_token = ''
    main_pain = save_path + '/' + author_name + '_' + project_name
    
    print("-----start crawling for %s-----" % project_name)

    if current_app.config['ALLOW_UPDATE'] or (not os.path.exists(main_pain + '/repo_info.json')) or (not os.path.exists(main_pain + '/forks.json')):
        repo_info = get_api(author_name, project_name, '', access_token)
        localfile_tool.write_to_file(main_pain + '/repo_info.json', repo_info)

        forks_list = get_api(author_name, project_name, 'forks', access_token)
        localfile_tool.write_to_file(main_pain + '/forks.json', forks_list)

    print("-----finish crawling for %s-----" % project_name)

    """
    # Get all forks' commits.
    for fork in forks_list:
        author, repo = fork["full_name"].split('/')
        commits_list = get_api(author, repo, "commits", access_token)
        localfile_tool.write_to_file(main_pain + '/' + author + '/commits.json', commits_list)
    """

"""
if __name__ == '__main__':
    project_info_crawler('shuiblue/INFOX')
"""

