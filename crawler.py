import requests
import json
import os

author_name = 'shuiblue'
project_name = 'INFOX'
access_token = ''

base_url = 'https://api.github.com/repos/%s/%s'
base_url_with_page = 'https://api.github.com/repos/%s/%s/%s?page=%d'
api_limit_error = 'API rate limit exceeded'
save_path = './tmp/%s_%s'

def write_to_file(file, obj):
    path = os.path.dirname(file)
    if not os.path.exists(path):
        os.makedirs(path)
    print ('start write result to file....')
    with open(file, 'w') as f:
        f.write(json.dumps(obj))
    print ('finish writing!')

# type contains: forks, branches, commits.
# page_iter means it will get all the items.
def get_api(author, repo, type = "", page_iter = True):
    if(not page_iter):
        try:
            response = requests.get(base_url % (author, repo))
            if(api_limit_error in response.text):
                raise Exception(api_limit_error)
        except requests.RequestException as e:
            print(e)
        return response.json()
    page_num = 0
    result = []
    while (True):
        page_num += 1
        print('page_num = %d' % page_num)
        try:
            response = requests.get(base_url_with_page % (author, repo, type, page_num))
            if (api_limit_error in response.text):
                raise Exception(api_limit_error)
        except requests.RequestException as e:
            print(e)
        list = response.json()
        if (len(list) == 0):
            break
        for item in list:
            result.append(item)
    print ('finish crawling! Get %d %s !' % (len(result), type))
    return result

def main():
    main_pain = save_path % (author_name, project_name)

    repo_info = get_api(author_name, project_name, "", False)
    print ('forks number: %d' % repo_info["forks"])
    print ('language is %s' % repo_info["language"])
    print ('description: %s' % repo_info["description"])
    write_to_file(main_pain + '/repo_info.txt', repo_info)

    repo_info_list = ['forks', 'branches', 'commits', 'comments']
    for info_type in repo_info_list:
        info_list = get_api(author_name, project_name, info_type)
        write_to_file(main_pain + '/' + info_type + '.txt', info_list)

    # get all forks' commits
    for fork in forks_list:
        author, repo = fork["full_name"].split('/')
        commits_list = get_api(author, repo, "commits")
        write_to_file(main_pain + '/' + author + '/commits.txt', commits_list)

if __name__ == '__main__':
    main()

