import requests
import json

author_name = 'shuiblue'
project_name = 'INFOX'

base_url = 'https://api.github.com/repos/%s/%s'
base_url_with_page = 'https://api.github.com/repos/%s/%s/%s?page=%d'
save_path = './tmp/%s/%s'

def write_to_file(file, obj)
    print ('start write result to file....')
    with open(file, 'w') as f:
        f.write(json.dumps(result))
    print ('finish writing!')

# type contains: forks, branches, commits.
# page_iter means it will get all the items.
def get_api(author, repo, type = "", page_iter = True):
    if(not page_iter):
        try:
            response = requests.get(base_url % (author, repo))
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
        except requests.RequestException as e:
            print(e)
        list = response.json()
        if (len(list) == 0):
            break
        for item in list:
            result.append(item)
    print ('finish crawling! Get %d %s !' % (len(result), type))
    

def main():
    repo_info = get_api(author_name, project_name, "", False)
    print ('forks number: %d' % repo_info["forks"])
    print ('language is %s' % repo_info["language"])
    print ('description: %s' % repo_info["description"])
    forks_list = get_api(author_name, project_name, 'forks')
    branches_list = get_api(author_name, project_name, 'branches')

    write_to_file((save_path % (author, repo)) + '/repo_info.txt', repo_info)
    write_to_file((save_path % (author, repo)) + '/' + type + '.txt', forks_list)

if __name__ == '__main__':
    main()

