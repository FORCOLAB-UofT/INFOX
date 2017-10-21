'''
This crawler is used for get the data of the repo from Github's API.
'''

import os
import json
import requests

# Following three lines can be setting by config
author_name = 'shuiblue'
project_name = 'INFOX'
# Github's API has limit, so it need your personal access token.
access_token = 'your_personal_access_token'

save_path = './tmp/%s_%s' # The data store in tmp/author_repo/
commits_page_limit = 1 # 1 is just for checking the status, if you need more commits set it larger. 

base_url = 'https://api.github.com/repos/%s/%s?access_token=%s'
base_url_with_page = 'https://api.github.com/repos/%s/%s/%s?page=%d&access_token=%s'

api_limit_error = 'API rate limit exceeded'

# Write the obj as json to file (overwrite if it exist).
# It will create the folder if it doesn't exist.
def write_to_file(file, obj):
    path = os.path.dirname(file)
    if not os.path.exists(path):
        os.makedirs(path)
    print 'start write %s to file....' % file
    with open(file, 'w') as write_file:
        write_file.write(json.dumps(obj))
    print 'finish writing!'

# get_api is the general function to get the data using Github's API.
# You can set author(like FancyCoder0), repo(like INFOX), type(forks, branches, commits).
# page_iter is need when type is not empty, which means whether the data is iterated(like get all the forks for the repo), this function will get all the items.
# Example:
#     get_api('FancyCoder0', 'INFOX', "", False)
#     get_api('FancyCoder0', 'INFOX', "forks", True)

def get_api(author, repo, type="", page_iter=True):
    if not page_iter:
        try:
            response = requests.get(base_url % (author, repo, access_token))
            if api_limit_error in response.text:
                raise Exception(api_limit_error)
        except requests.RequestException as error:
            print(error)
        return response.json()
    page_num = 0
    result = []
    while True:
        page_num += 1

        # This is manual limit to speed up checking the status.
        if type == "commits" and page_num > commits_page_limit:
            break

        # print('page_num = %d' % page_num)
        try:
            response = requests.get(base_url_with_page % (author, repo, type, page_num, access_token))
            if api_limit_error in response.text:
                raise Exception(api_limit_error)
        except requests.RequestException as error:
            print(error)

        json_result = response.json()

        if not json_result:
            break

        for item in json_result:
            result.append(item)

    print 'finish crawling! Get %d %s !' % (len(result), type)
    return result

def main():
    main_pain = save_path % (author_name, project_name)

    repo_info = get_api(author_name, project_name, "", False)
    write_to_file(main_pain + '/repo_info.json', repo_info)

    forks_list = get_api(author_name, project_name, 'forks')
    write_to_file(main_pain + '/forks.json', forks_list)

    # get all forks' commits
    for fork in forks_list:
        author, repo = fork["full_name"].split('/')
        commits_list = get_api(author, repo, "commits")
        write_to_file(main_pain + '/' + author + '/commits.json', commits_list)

if __name__ == '__main__':
    main()

