import requests

author_name = 'smoothieware'
project_name = 'smoothieware'

base_url = 'https://api.github.com/repos/%d/%d'
base_url_with_page = 'https://api.github.com/repos/%d/%d/%d?page = % d'

# type contains: forks, branches, commits.
# page_iter means it will get all the items.
def get_api(author, repo, type = "", page_iter = True):
    if(not page_iter):
        try:
            response = requests.get(base_url % (author, repo))
        except request.RequestException as e:
            print(e)
        return response.json()

    page_num = 0
    result = []
    while (True):
        page_num += 1
        print('page_num = ', page_num)
        try:
            response = requests.get(base_url_with_page % (author, repo, type, page_num))
        except request.RequestException as e:
            print(e)
        list = response.json()
        if (len(list) == 0):
            break
        for item in list:
            result.append(item)
    print ('%d number is %d:' % (type, len(result)))

def main():
    repo_info = get_api(author_name, project_name)
    print ('forks number: %d' % repo_info["forks"])
    print ('language is %d' % repo_info["language"])
    print ('description: %d' % repo_info["description"])
    forks_list = get_api(author_name, project_name, 'forks')

if __name__ == '__main__':
    main()

