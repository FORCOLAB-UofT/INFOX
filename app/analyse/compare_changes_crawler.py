import os
import re
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

from .util import language_tool


def fetch_commit_list(repo, fork, default_branch="master"):
    commit_list = []
    # todo find correct url for different branches. Here we make the assumption we are comparing master branches
    # later on might have to change to main
    url = "https://github.com/%s/compare/%s...%s:%s" % (
        repo,
        default_branch,
        fork,
        default_branch
    )
    s = requests.Session()
    s.mount("https://github.com", HTTPAdapter(max_retries=5))

    try:
        diff_page = s.get(url, timeout=250)
        if diff_page.status_code != requests.codes.ok:
            raise Exception("error on fetch compare page on %s!" % repo)
    except:
        # raise Exception("error on fetch compare page on %s!" % repo)
        return []
    diff_page_soup = BeautifulSoup(diff_page.content, "html.parser")
    for commit in diff_page_soup.find_all(
        "a", {"class": "Link--primary text-bold js-navigation-open markdown-title"}
    ):
        href = commit.get("href")
        if "https://" not in href:
            href = "https://github.com" + href
        title = commit.text
        commit_list.append({"title": title, "link": href})
    return commit_list


def fetch_diff_code(repo, fork, default_branch="master"):
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
    url = "https://github.com/%s/compare/%s...%s:%s" % (
        repo,
        default_branch,
        fork,
        default_branch
    )
    # It will first jump to https://github.com/author/repo/compare/version...author:repo,
    # then fetch from https://github.com/author/repo/compare/version...author:repo.patch
    try:
        url = requests.get(url, timeout=120).url + ".diff"
        r = requests.get(url, timeout=120)
        if r.status_code != requests.codes.ok:
            raise Exception("error on fetch compare page on %s!" % repo)
    except:
        #raise Exception("error on fetch compare page on %s!" % repo)
        return []

    diff_list = r.text.split("diff --git")
    for diff in diff_list[1:]:
        try:
            file_full_name = re.findall("a\/.*? b\/(.*?)\n", diff)[0]
            file_name, file_suffix = os.path.splitext(file_full_name)
        except:
            continue

        if not language_tool.is_text(file_full_name):
            file_list.append(
                {
                    "file_full_name": file_full_name,
                    "file_suffix": file_suffix,
                    "diff_link": "#",
                    "added_line": 0,
                    "added_code": None,
                }
            )
            continue

        st = re.search("@@.*?-.*?\+.*?@@", diff)
        if st is None:
            continue

        parts = re.split("@@.*?-.*?\+.*?@@", diff[st.start() :])
        start_with_plus_regex = re.compile("^\++")
        start_with_minus_regex = re.compile("^\-+")

        diff_code = ""
        diff_code_line = 0
        for part in parts:
            # only filter added code
            added_lines_of_code = filter(
                lambda x: (x) and (x[0] == "+"), part.splitlines()
            )
            added_lines_of_code = [
                start_with_plus_regex.sub("", x) for x in added_lines_of_code
            ]

            deleted_lines_of_code = filter(
                lambda x: (x) and (x[0] == "-"), part.splitlines()
            )
            deleted_lines_of_code = [
                start_with_minus_regex.sub("", x) for x in deleted_lines_of_code
            ]

            diff_code += "\n".join(added_lines_of_code) + "\n"
            diff_code_line += len(added_lines_of_code)

        # TODO change diff_link to code position
        file_list.append(
            {
                "file_full_name": file_full_name,
                "file_suffix": file_suffix,
                "diff_link": "#",
                "added_line": diff_code_line,
                "added_code": diff_code,
            }
        )
    return file_list


def fetch_compare_page(repo_name, fork_name):
    """Compare the fork with the main repo.
    Return:
        A dict contains following fields :
        compare_result {
            changed_file_number,
            total_changed_line_number,

    """
    print("START fetch fork: ", fork_name)
    try:
        commit_list = fetch_commit_list(repo_name, fork_name)
        file_list = fetch_diff_code(repo_name, fork_name)
    except:
        print("FAILED on fetch fork: ", fork_name)
        return None

    print("SUCCESS on fetch fork: ", fork_name)
    return {"file_list": file_list, "commit_list": commit_list}


if __name__ == "__main__":
    # Used for testing
    # print(fetch_diff_code('shuiblue/INFOX-1'))
    # fetch_compare_page('Nutz95/Smoothieware')
    # fetch_compare_page('mkosieradzki/protobuf')
    t = fetch_compare_page("SkyNet3D/Marlin")
    for i in t["file_list"]:
        print(i["file_full_name"])
    for i in t["commit_list"]:
        print(i["title"], i["link"])
    # fetch_compare_page('aJanker/TypeChef')
