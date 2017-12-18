import os
import re
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

from .util import language_tool

def fetch_commit_list(project_full_name):
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
    url = 'https://github.com/%s/compare' % project_full_name

    driver = webdriver.PhantomJS(
        service_args=['--ignore-ssl-errors=true', '--ssl-protocol=tlsv1'])
    # driver = webdriver.PhantomJS()
    try:
        # It will jump to https://github.com/author/repo/compare/version...author:repo
        driver.get(url)
    except:
        raise Exception('error on fetch compare page on %s' % project_full_name)

    commit_list = []
    try:
        commit_list_on_page = driver.find_elements_by_class_name('commit-message ')
        for commit in commit_list_on_page:
            href = commit.find_element_by_class_name('message').get_attribute('href')
            soup = BeautifulSoup(requests.get(href).content, 'html.parser')
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
                print("fetch" + author + "'s commit")
    except:
        print("Can not get commit list!")

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
    url = 'https://github.com/%s/compare' % project_full_name
    # It will first jump to https://github.com/author/repo/compare/version...author:repo,
    # then fetch from https://github.com/author/repo/compare/version...author:repo.patch
    url = requests.get(url).url + '.patch'
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        content = r.text
    else:
        raise Exception('error on fetch compare page on %s!' % project_full_name)
    
    diff_list = content.split('diff --git')
    file_list = []
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
        diff_code = ""
        diff_code_line = 0
        for part in parts:
            # only filter added code
            lines_of_code = filter(lambda x: (x) and (x[0] == '+'), part.splitlines())
            lines_of_code = [start_with_plus_regex.sub('', x) for x in lines_of_code]
            diff_code += '\n'.join(lines_of_code) + '\n'
            diff_code_line += len(lines_of_code)
        
        # TODO change diff_link to code position
        file_list.append({"file_full_name": file_full_name, "file_suffix": file_suffix,
                          "diff_link": '#', "added_line": diff_code_line, "added_code": diff_code})
    return file_list
    

def fetch_compare_page(project_full_name):
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
    commit_list = fetch_commit_list(project_full_name)
    file_list = fetch_diff_code(project_full_name)

    return {"file_list": file_list,
            "commit_list": commit_list}

"""
if __name__ == '__main__':
    # Used for testing
    # fetch_compare_page('Nutz95/Smoothieware')
    #fetch_compare_page('mkosieradzki/protobuf')
    fetch_compare_page('SkyNet3D/Marlin')
    #fetch_compare_page('aJanker/TypeChef')
"""
