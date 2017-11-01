"""
This crawler is used for get the data of the repo from Github's API.
"""

import os
import json
import requests
import ConfigParser

commits_page_limit = 1 # 1 is just for checking the status, if you need more commits set it larger.

base_url = 'https://api.github.com/repos/%s/%s'
base_url_with_page = 'https://api.github.com/repos/%s/%s/%s?page=%d'
api_limit_error = 'API rate limit exceeded'

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
    print 'start write %s to file....' % file
    with open(file, 'w') as write_file:
        write_file.write(json.dumps(obj))
    print 'finish writing!'

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
        print 'finish crawling!'
        return response.json()

    page_num = 0
    result = []
    # Do the loop until getting the empty response.
    while True:
        page_num += 1

        # This is manual limit to speed up checking the status.
        if type == "commits" and page_num > commits_page_limit:
            break

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

    print 'finish crawling! Get all the %s !' % (type)
    return result

def main():
    conf = ConfigParser.ConfigParser()
    conf.read('./config.conf')
    # Following args is set by config
    author_name = conf.get("repo_info", "owner")
    project_name = conf.get("repo_info", "repo")
    save_path = conf.get("location", "save_path")
    access_token = conf.get("token", "access_token")

    main_pain = save_path + '/' + author_name + '_' + project_name
    
    repo_info = get_api(author_name, project_name, '', access_token)
    write_to_file(main_pain + '/repo_info.json', repo_info)

    forks_list = get_api(author_name, project_name, 'forks', access_token)
    write_to_file(main_pain + '/forks.json', forks_list)

    # get all forks' commits
    for fork in forks_list:
        author, repo = fork["full_name"].split('/')
        commits_list = get_api(author, repo, "commits", access_token)
        write_to_file(main_pain + '/' + author + '/commits.json', commits_list)

if __name__ == '__main__':
    main()

