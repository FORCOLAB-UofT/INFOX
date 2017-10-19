import os
from selenium import webdriver
import requests

language_file_suffix = ['.h', '.c', '.cc', '.cpp', '.java']
stop_words = [',', '(', ')', ';', '.']

# Example:
#     compare('NeilBetham/Smoothieware')
#     It will return 26.
def compare(project_full_name):
    # It will jump to https://github.com/author/repo/compare/version...author:repo
    print "start : ", project_full_name
    url = 'https://github.com/%s/compare' % project_full_name
    driver = webdriver.PhantomJS()
    try:
        driver.get(url)
        repo_content = driver.find_element_by_class_name("repository-content")
    except:
        print "error on get diff for %s!" % project_full_name
        return (-1, -1)
    # TODO(Luyao Ren) some page is loading dynamic
    # Example: https://github.com/Smoothieware/Smoothieware/compare/edge...Nutz95:edge

    # If the changed is too large, the result from github will
    # not show diff code first.
    # Example: https://github.com/Smoothieware/Smoothieware/compare/edge...briand:edge
    try:
        flag_too_large = True
        repo_overall_info = repo_content.find_element_by_class_name("tabnav")
    except:
        flag_too_large = False

    # changed_file_list = []
    total_changed_line_of_source_code = -1
    if(not flag_too_large):
        try:
            diff_list = repo_content.find_element_by_id("diff").find_element_by_id("files")
        except:
            return (0, 0)
        changed_file_number = 0
        total_changed_line_of_source_code = 0
        diff_num = 0
        while True:
            diff = diff_list.find_element_by_id('diff-' + str(diff_num))

            diff_num += 1
            diff_info = diff.find_element_by_class_name('file-info')
            diff_info_split = diff_info.text.split(' ')
            changed_line = diff_info_split[0]
            file = diff_info_split[1]
            # changed_file_list.append(file)
            try:
                total_changed_line_of_source_code += int(changed_line)
                changed_file_number += 1
            except:
                pass
            file_name, file_suffix = os.path.splitext(file)
            if file_suffix in language_file_suffix:
                changed_code = diff.text
                # This is for the case that "Large diffs are not rendered by default" on Github
                # Example: https://github.com/MarlinFirmware/Marlin/compare/1.1.x...SkyNet3D:SkyNet3D-Devel
                try:
                    load_container = diff.find_element_by_class_name('js-diff-load-container')
                    print "This file: %s need load code." % file
                    load_url = load_container.find_element_by_xpath('//include-fragment[1]') \
                        .get_attribute('data-fragment-url')
                    try:
                        changed_code = requests.get('https://github.com/' + load_url).text
                    except:
                        print "Error on get load code!"
                except:
                    pass

                word_lists = changed_code.split(' ')
                word_lists = filter(lambda x: (len(x) >= 2) and (x not in stop_words), word_lists)
                # print "word lists (after filter):", word_lists
        # print "changed file list:", changed_file_list
    else:
        commits, changed_files, comments = repo_overall_info.find_elements_by_class_name('Counter')
        changed_file_number = int(changed_files.text)

    # print("total changed line = %d" % total_changed_line_of_source_code)
    return (changed_file_number, total_changed_line_of_source_code)
