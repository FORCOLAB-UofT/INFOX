import os
import re
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

from .util import language_tool

def fetch_commit_list_by_api(fork_project_full_name, upstream_project_full_name):
    """
    Args:
        fork_project_full_name: for example: 'shuiblue/INFOX-1',
        upstream_project_full_name: for example: 'luyaor/INFOX'
    Return:
        commit_list {
                author,
                title,
                description,
                link,
            }
    """

    try:
        url = 'https://github.com/%s/compare' % fork_project_full_name
        url = requests.get(url, timeout=120).url

        upstream_branch = url.split('...')[0].split('/')[-1]
        fork_branch = url.split(':')[-1]
        url = 'https://api.github.com/repos/%s/compare/%s...%s:%s' % (
        upstream_project_full_name, upstream_branch, fork_project_full_name.split('/')[0], fork_branch)

        r = requests.get(url, timeout=120)
        if r.status_code != requests.codes.ok:
            raise Exception('error on fetch commit in compare page on %s!' % fork_project_full_name)
    except:
        raise Exception('error on fetch commit compare page on %s!' % fork_project_full_name)

    r = r.json()

    commit_list = []

    # print(len(r['commits']))

    for commit in r['commits']:
        author = commit['commit']['author']['name']
        title = commit['commit']['message']
        desc = commit['commit']['message']
        link = commit['html_url']
        commit_list.append({
            "author":author,
            "title":title,
            "description":desc,
            "link":link
            })
    return commit_list


def fetch_commit_list(project_full_name): # Deprecated
    """
    Args:
        project_full_name: for example: 'NeilBetham/Smoothieware'
    Return:
        commit_list {
                author,
                title,
                description,
                link,
            }
    """
    commit_list = []

    url = 'https://github.com/%s/compare' % project_full_name
    s = requests.Session()
    s.mount('https://github.com', HTTPAdapter(max_retries=3))

    try:
        diff_page = s.get(url, timeout=120)
        if diff_page.status_code != requests.codes.ok:
            raise Exception('error on fetch compare page on %s!' % project_full_name)
    except:
        raise Exception('error on fetch compare page on %s!' % project_full_name)

    diff_page_soup = BeautifulSoup(diff_page.content, 'html.parser')
    for commit in diff_page_soup.find_all('a', {'class': 'commit-message'}):
        try:
            href = commit.get('href')
            if 'https://' not in href:
                href = 'https://github.com' + href
            soup = BeautifulSoup(s.get(href, timeout=120).content, 'html.parser')
        except:
            continue
        try:
            author = soup.find('a', {'class': 'user-mention'}).text
        except:
            author = ""
        try:
            title = soup.find('p', {'class': 'commit-title'}).text
        except:
            title = ""
        try:
            desc = soup.find('div', {'class': 'commit-desc'}).text
        except:
            desc = ""
        if author or title or desc or href:
            commit_list.append({
                "author":author,
                "title":title,
                "description":desc,
                "link":href
                })
    return commit_list


def fetch_diff_code(project_full_name):
    """
    Args:
        project_full_name: for example: 'NeilBetham/Smoothieware'
    Return:
        file_list {
                file_full_name,
                file_suffix,
                diff_link,
                added_line,
                added_code,
        }
    """
    file_list = []
    url = 'https://github.com/%s/compare' % project_full_name
    # It will first jump to https://github.com/author/repo/compare/version...author:repo,
    # then fetch from https://github.com/author/repo/compare/version...author:repo.patch
    try:
        url = requests.get(url, timeout=120).url + '.diff'
        r = requests.get(url, timeout=120)
        if r.status_code != requests.codes.ok:
            raise Exception('error on fetch compare page on %s!' % project_full_name)
    except:
        raise Exception('error on fetch compare page on %s!' % project_full_name)

    diff_list = r.text.split('diff --git')
    for diff in diff_list[1:]:
        try:
            file_full_name = re.findall('a\/.*? b\/(.*?)\n', diff)[0]
            file_name, file_suffix = os.path.splitext(file_full_name)
        except:
            continue

        if not language_tool.is_text(file_full_name):
            file_list.append({"file_full_name": file_full_name, "file_suffix": file_suffix,
                              "diff_link": '#', "added_line": 0, "added_code": None})
            continue

        st = re.search('@@.*?-.*?\+.*?@@', diff)
        if st is None:
            continue

        parts = re.split('@@.*?-.*?\+.*?@@', diff[st.start():])
        start_with_plus_regex = re.compile('^\++')
        start_with_minus_regex = re.compile('^\-+')
        
        diff_code = ""
        diff_code_line = 0
        for part in parts:
            # only filter added code
            added_lines_of_code = filter(lambda x: (x) and (x[0] == '+'), part.splitlines())
            added_lines_of_code = [start_with_plus_regex.sub('', x) for x in added_lines_of_code]

            deleted_lines_of_code = filter(lambda x: (x) and (x[0] == '-'), part.splitlines())
            deleted_lines_of_code = [start_with_minus_regex.sub('', x) for x in deleted_lines_of_code]

            diff_code += '\n'.join(added_lines_of_code) + '\n'
            diff_code_line += len(added_lines_of_code)
        
        # TODO change diff_link to code position
        file_list.append({"file_full_name": file_full_name, "file_suffix": file_suffix,
                          "diff_link": '#', "added_line": diff_code_line, "added_code": diff_code})
    return file_list
    

def fetch_compare_page(project_full_name, upstream_full_name):
    """Compare the fork with the main branch.
    Args:
        project_full_name: for example: 'NeilBetham/Smoothieware'
    Return:
        A dict contains following fields :
        compare_result {
            changed_file_number,
            total_changed_line_number,
            
    """
    print('start fetch fork: ', project_full_name)
    commit_list = fetch_commit_list_by_api(project_full_name, upstream_full_name)
    file_list = fetch_diff_code(project_full_name)

    return {"file_list": file_list,
            "commit_list": commit_list}


if __name__ == '__main__':
    # Used for testing
    # print(fetch_diff_code('shuiblue/INFOX-1'))
    # fetch_compare_page('Nutz95/Smoothieware')
    #fetch_compare_page('mkosieradzki/protobuf')

    # t = fetch_compare_page('SkyNet3D/Marlin')
    # for i in t["file_list"]:
    #     print(i["file_full_name"])
    # for i in t["commit_list"]:
    #     print(i["title"])
    # t = fetch_commit_list_by_api('fdintino/nginx-upload-module', 'ilya-maltsev/nginx-upload-module')

    t = fetch_commit_list_by_api('shuiblue/INFOX-1', 'luyaor/INFOX')
    # t = fetch_compare_page('yoft/Smoothieware', 'Smoothieware/Smoothieware')
    for x in t:
        print(x['title'])

