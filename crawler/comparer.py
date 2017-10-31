import os
from selenium import webdriver
import requests
import nltk

def compare(project_full_name):
    """Compare the fork with the main branch.
    Args:
        project_full_name: for example: 'NeilBetham/Smoothieware'
    Return:
        A dict contains this :
        compare_result {
            changed_file_number,
            total_changed_line_number,
            file_list {
                file_full_name,
                file_suffix,
                changed_line,
                changed_code,
                tokens,
            }
    """
    
    # load stop words
    stop_words = []
    with open('./data/cplusplus_stopwords.txt') as f:
        for line in f.readlines():
            word = line.strip()
            if word:
                stop_words.append(word)

    # load language suffix
    language_file_suffix = []
    with open('./data/cplusplus_stopwords.txt') as f:
        for line in f.readlines():
            suffix = line.strip();
            if suffix:
                language_file_suffix.append(suffix)


    print "start : ", project_full_name
    url = 'https://github.com/%s/compare' % project_full_name
    # It will jump to https://github.com/author/repo/compare/version...author:repo
    url = requests.get(url).url
    url.append('.patch')
    r = reuqests.get(url)
    if r.status_code == requests.codes.ok:
        content = r.content
    else:
        print "error on get diff for %s!" % project_full_name
        return {"changed_line": -1,
                "changed_file_number": -1,
                "file_list": []}

    file_list = []
    diff_list = content.split('diff -- git')

    # changed_file_number = 0
    # total_changed_line_of_source_code = 0
    # diff_num = 0

    # re.sub("@@*+@@","")
    # 取出注释 
    #
    for diff in diff_list:
        file_full_name = diff.first_line
        file_name, file_suffix = os.path.splitext(file_full_name)

        diff_num += 1
        changed_code = []
        code = re.split('@@\.@@', diff)
        add_line = 0
        delete_line = 0
        for code_line in code:
            if code_line[0] == '+':
                code_line = code_line[1:]
                add_line += 1
                changed_code.append(code_line)
            elif code_line[0] == '-':
                delete_line += 1
        
        if file_suffix in language_file_suffix:
            # process on changed code
            # get the tokens from changed code
            tokens = filter(lambda x: (len(x) > 1) and (x not in stop_words), nltk.word_tokenize(changed_code))
            file_list.append({"file_full_name": file_full_name, "file_suffix": file_suffix,
                              "changed_line": changed_line, "changed_code": changed_code, "tokens": tokens})

    # print "changed file list:", changed_file_list
    # print("total changed line = %d" % total_changed_line_of_source_code)

    return {"changed_line": total_changed_line_of_source_code,
            "changed_file_number": changed_file_number,
            "file_list": file_list}
