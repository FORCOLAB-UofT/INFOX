import os
import json
from collections import Counter
import ConfigParser
import codecs
import re
import nltk
from nltk.stem.porter import PorterStemmer

import compare_changes_crawler

FLAGS_CRAWLER_MODE = False # If you need crawler offline, change it true and run analyser individually.
if not FLAGS_CRAWLER_MODE:
    from ..models import Project, ProjectFork, ChangedFile


language_list = []
language_file_suffix = {}
language_stop_words = {}

def write_to_file(file, obj):
    """ Write the obj as json to file.
    It will overwrite the file if it exist
    It will create the folder if it doesn't exist.
    Args:
        file: the file's path, like : ./tmp/INFOX/repo_info.json
        obj: the instance to be written into file (can be list, dict)
    Return:
        none
    """
    path = os.path.dirname(file)
    if not os.path.exists(path):
        os.makedirs(path)
    print 'start write %s to file....' % file
    with open(file, 'w') as write_file:
        write_file.write(json.dumps(obj))
    print 'finish writing!'

def get_repo_info(main_path):
    """ Get the info of repo.
    Args:
        main_path: the file store location.
    Return:
        A json object.
    """
    with open(main_path + '/repo_info.json') as read_file:
        repo_info = json.load(read_file)
    return repo_info

def get_forks_info_dict(main_path):
    """ Get the info of fork.
    It includes language, description, forks number.

    Args:
        main_path: the file store location.
    Return:
        A dict contains information of the forks.
        The key is fork's full name, the value is a dict of fork's information.
    """
    # print '---------------------------------------'
    forks_info = {}
    with open(main_path + '/forks.json') as read_file:
        forks_list = json.load(read_file)
        for fork in forks_list:
            fork_name = fork["full_name"].split('/')[0]
            forks_info[fork_name] = fork
    return forks_info

"""
def get_forks_list(main_path):
    # Get the list of forks and it's last committed time.
    #Args:
    #    main_path: the file store location.
    #Return:
    #    A list of tuple of fork's full name and last committed time.
    
    forks = []
    dir_list = os.listdir(main_path)
    for dir in dir_list:
        if os.path.isdir(main_path + '/' + dir):
            with open(main_path + '/' + dir + '/commits.json') as read_file:
                commits = json.load(read_file)
                try:
                    date = commits[0]["commit"]["committer"]["date"]
                    forks.append((dir, date))
                except:
                    pass
                    # print "missing commit on %s" % dir
    return forks
"""

def word_filter(word):
    """ The filter used for deleting the noisy words in changed code.
    Here is the method:
        1. Delete character except for digit, alphabet, '_'.
        2. the word shouldn't be all digit.
        3. the length should large than 2.
    Args:
        word
    Return:
        True for not filtering, False for filtering.
    """
    word = re.sub("[^0-9A-Za-z_]", "", word)
    if(word.isdigit()):
        return False
    if(len(word) <= 2):
        return False
    return True

def load_project(project_name):
    # you need to change following paths manully.
    current_path = '/Users/fancycoder/infox/app/analyse' # the current path
    local_data_path = '/Users/fancycoder/infox_data/result' # the same with save_path in crawler/config.conf
    # result_file = "/Users/fancycoder/infox_data/result/tmp_result.txt" # the local file for overview of all the forks.
    
    main_path = local_data_path + "/" + project_name

    with open(current_path + '/data/support_language.txt') as read_file:
        for line in read_file.readlines():
            if line:
                language = line.strip()
                language_list.append(language)
                language_file_suffix[language] = []
                language_stop_words[language] = []
                with open(current_path + '/data/' + language + '_suffix.txt') as f:
                    for line in f.readlines():
                        if line:
                            suffix = line.strip()
                            language_file_suffix[language].append(suffix)
                with open(current_path + '/data/' + language + '_stopwords.txt') as f:
                    for line in f.readlines():
                        if line:
                            word = line.strip()
                            language_stop_words[language].append(word)

    repo_info = get_repo_info(main_path)

    """
    # Write the infomation of repo.
    # It includes language, description, forks number.
    print "---------------------------------------"
    with open(result_file, 'w') as write_file:
        write_file.write(repo_info["full_name"] + "\n")
    for type in ["language", "description", "forks"]:
        out_result = type + " : " + str(repo_info[type]) + "\n"
        print out_result
        with codecs.open(result_file, 'a', 'utf-8') as write_file:
            write_file.write(out_result)
    """

    if not FLAGS_CRAWLER_MODE:
        # Load project into database.
        Project(
            project_name 		= project_name,
            language 			= repo_info["language"],
            fork_number 		= repo_info["forks"],
            description         = str(repo_info["description"]),
        ).save();

    forks_info = get_forks_info_dict(main_path)

    # forks = get_forks_list(main_path)
    # forks.sort(key=lambda x: x[1], reverse=True) # sort fork by last committed time

    # print "---------------------------------------"
    for author in forks_info:
        fork_name = forks_info[author]["full_name"]
        created_time = forks_info[author]["created_at"]
        last_committed_time = forks_info[author]["pushed_at"]
        # Ignore the fork if it doesn't have commits after fork.
        if last_committed_time <= created_time:
            continue
        # Load the result in local file.
        result_path = main_path + '/' + author + '/result.json'
        if os.path.exists(result_path):
            with open(result_path) as read_file:
                compare_result = json.load(read_file)
        else:
            if FLAGS_CRAWLER_MODE:
                # If the compare result is not crawled, start to crawl.
                compare_result = compare_changes_crawler.compare(fork_name)
                if(compare_result["changed_file_number"] == -1):
                    continue
                write_to_file(result_path, compare_result)
            else:
                continue

        # Ignore the fork if it is not changed.
        if compare_result["changed_line"] == 0:
            continue

        # Output & Save the overview of this fork.
        out_result = ("fork_author: %18s, last committed time : %15s, "
                    "created time: %15s, changed file: %3d, changed code line: %4d\n" %
                    (author, last_committed_time, created_time,
                    compare_result["changed_file_number"],
                    compare_result["changed_line"]))
        
        """
        print out_result.strip()
        with codecs.open(result_file, 'a', 'utf-8') as write_file:
            write_file.write(out_result)
        """

        # Output & Save the changed file list of this fork.
        all_tokens = []
        all_stemmed_tokens = []
        file_list = []

        for file in compare_result["file_list"]:
            file_name = file["file_full_name"]
            file_suffix = file["file_suffix"]
            changed_code = file["changed_code"]
            changed_line = file["changed_line"]
            common_tokens = []
            common_stemmed_tokens = []

            file_language = ""
            
            # Check the language depend on the file suffix.
            for language in language_list:
                if(file_suffix in language_file_suffix[language]):
                    file_language = language
    
            if file_language:
                # process on changed code
                # get the tokens from changed code
                tokens = filter(lambda x: (len(x) > 1) and (x not in language_stop_words[file_language]), nltk.word_tokenize(changed_code))
                tokens = filter(word_filter, tokens)
                stemmed_tokens = [PorterStemmer().stem(word) for word in tokens] # do stem on the tokens

                for x in tokens:
                    all_tokens.append(x)
                for x in stemmed_tokens:
                    all_stemmed_tokens.append(x)

                common_tokens = [x[0] for x in Counter(tokens).most_common(10)]
                common_stemmed_tokens = [x[0] for x in Counter(stemmed_tokens).most_common(10)]

                # load current file's name, key words to fork.
                file_list.append(file_name)
            else:
                file_language = "Unsupported"
            
            if not FLAGS_CRAWLER_MODE:
                # Load changed files into database.
                ChangedFile(
                    full_name = project_name + '/' + fork_name + '/' + file_name,
                    file_name = file_name,
                    fork_name = fork_name,
                    project_name = project_name,
                    file_language = file_language,
                    file_suffix = file_suffix,
                    # changed_code = file["changed_code"],
                    changed_line_number = changed_line,
                    key_words = common_tokens,
                    key_stemmed_words = common_stemmed_tokens,
                    # variable 
                    # class_name 
                    # function_name 
                ).save()
            
            """
            print file_name , ":", common_tokens
            with codecs.open(result_file, 'a', 'utf-8') as write_file:
                write_file.write(full_name + ":\n")
                write_file.write('%35s' % 'common tokens: ')
                write_file.write(json.dumps(common_tokens))
                write_file.write('\n')
                write_file.write('%35s' % 'common tokens after stemming: ')
                write_file.write(json.dumps(common_stemmed_tokens))
                write_file.write('\n')
                write_file.write('\n')
            """

        # sorted_key_words = sorted(key_words.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        
        if not FLAGS_CRAWLER_MODE:
            key_words = [x[0] for x in Counter(all_tokens).most_common(20)]
            key_stemmed_words = [x[0] for x in Counter(all_stemmed_tokens).most_common(20)]
            # Load forks into database.
            ProjectFork(
                full_name = project_name + '/' + fork_name,
                fork_name = fork_name,
                project_name = project_name,
                total_changed_file_number = compare_result["changed_file_number"],
                total_changed_line_number = compare_result["changed_line"],
                last_committed_time = last_committed_time,
                created_time = created_time,
                file_list = file_list,
                key_words = key_words,
                key_stemmed_words = key_stemmed_words
            ).save();
        

if __name__ == '__main__':
    print "Input the project name"
    project_name = raw_input().strip()
    load_project(project_name)
