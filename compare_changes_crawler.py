import os
from selenium import webdriver
import requests
import nltk
from nltk.stem.porter import PorterStemmer

language_file_suffix = ['.h', '.c', '.cc', '.cpp', '.hpp']
stop_words = []

'''
Example:
    compare('NeilBetham/Smoothieware')
    It will return compare_result which looks like:
    compare_result {
    changed_file_number,
    total_changed_line_number,
    file_list {
      file_full_name,
      file_suffix,
      changed_line,
      changed_code,
      tokens,
      stemmed_tokens,
    }
'''

def do_stemming(filtered):
	stemmed = []
	for f in filtered:
		stemmed.append(PorterStemmer().stem(f))
	return stemmed

def compare(project_full_name):
    # load stop words
    with open('./data/cplusplus_stopwords.txt') as f:
        for line in f.readlines():
            word = line.strip()
            stop_words.append(word)

    print "start : ", project_full_name
    # It will jump to https://github.com/author/repo/compare/version...author:repo
    url = 'https://github.com/%s/compare' % project_full_name
    driver = webdriver.PhantomJS()
    try:
        driver.get(url)
        repo_content = driver.find_element_by_class_name("repository-content")
    except:
        print "error on get diff for %s!" % project_full_name
        return {"changed_line": -1,
                "changed_file_number": -1,
                "file_list": []}

    try:
        # If the changed is too large, the result from github will not show diff code first.
        # Example: https://github.com/Smoothieware/Smoothieware/compare/edge...briand:edge
        repo_overall_info = repo_content.find_element_by_class_name("tabnav")
        commits, changed_files, comments = repo_overall_info.find_elements_by_class_name('Counter')
        changed_file_number = int(changed_files.text)
        return {"changed_line": -1,
                "changed_file_number": changed_file_number,
                "file_list": []}
        # repo_content = driver.find_element_by_class_name('repository-content')
    except:
        pass

    file_list = []
    total_changed_line_of_source_code = -1
    try:
        diff_list = repo_content.find_element_by_id("diff").find_element_by_id("files")
    except:
        return {"changed_line": 0,
                "changed_file_number": 0,
                "file_list": []}

    changed_file_number = 0
    total_changed_line_number = 0
    diff_num = 0
    # TODO(Luyao Ren) change to get the list of diff.
    # TODO(Luyao Ren) change analysis part using Beautiful Soup to speed up.
    while True:
        try:
            diff = diff_list.find_element_by_id('diff-' + str(diff_num))
            diff_num += 1
        except:
            try:
                # Some page is loading dynamic, so we need to get more diff.
                # Example: https://github.com/Smoothieware/Smoothieware/compare/edge...Nutz95:edge
                load_url = diff_list.find_element_by_tag_name('include-fragment').get_attribute('src')
                driver.get(load_url)
                diff_list = driver.find_element_by_tag_name('body')
                continue
            except:
                break

        diff_info = diff.find_element_by_class_name('file-info')
        changed_line = diff_info.text.split(' ')[0].strip().replace(',','')
        file_full_name = diff_info.text.split(' ')[1].strip()
        print diff_num, changed_line, file_full_name
        try:
            total_changed_line_of_source_code += int(changed_line)
            changed_file_number += 1
        except:
            changed_line = 0
            pass
        file_name, file_suffix = os.path.splitext(file_full_name)

        # TODO(Luyao Ren) add analysis on other files
        if file_suffix in language_file_suffix:
            changed_code = diff.text
            try:
                # This is for the case that "Large diffs are not rendered by default" on Github
                # Example: https://github.com/MarlinFirmware/Marlin/compare/1.1.x...SkyNet3D:SkyNet3D-Devel
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
            # process on changed code
            tokens = nltk.word_tokenize(changed_code)
            tokens = filter(lambda x: (len(x) > 1) and (x not in stop_words), tokens)
            stemmed_tokens = do_stemming(tokens)

            file_list.append({"file_full_name": file_full_name, "file_suffix": file_suffix,
                              "changed_line": changed_line, "changed_code": changed_code,
                              "tokens": tokens, "stemmed_tokens": stemmed_tokens})

    # print "changed file list:", changed_file_list
    # print("total changed line = %d" % total_changed_line_of_source_code)
    return {"changed_line": total_changed_line_of_source_code,
            "changed_file_number": changed_file_number,
            "file_list": file_list}
