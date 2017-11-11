import os
import json
from collections import Counter
import configparser
import codecs
import re
import datetime
import nltk
from nltk.stem.porter import PorterStemmer
import itertools

from flask import current_app
from ..crawler import compare_changes_crawler

FLAGS_APP_MODE = True

if FLAGS_APP_MODE:
    from ..models import Project, ProjectFork, ChangedFile

language_list = []
language_file_suffix = {}
language_stop_words = {}

def load_language_data(language_data_path):
    with open(language_data_path + '/support_language.txt') as read_file:
        for line in read_file.readlines():
            if line:
                language = line.strip()
                language_list.append(language)
                language_file_suffix[language] = []
                language_stop_words[language] = []
                with open(language_data_path + '/' + language + '_suffix.txt') as f:
                    for line in f.readlines():
                        if line:
                            suffix = line.strip()
                            language_file_suffix[language].append(suffix)
                with open(language_data_path + '/' + language + '_stopwords.txt') as f:
                    for line in f.readlines():
                        if line:
                            word = line.strip()
                            language_stop_words[language].append(word)

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
    with open(file, 'w') as write_file:
        write_file.write(json.dumps(obj))
    print ('finish write %s to file....' % file)

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

def word_split_by_char(s):
    words = []
    if '-' in s: # Case: ab-cd-ef
        words = s.split('-')
    elif '.' in s: # Case: ab.cd.ef
        words = s.split('.')
    elif '_' in s: # Case: ab_cd_ef
        words = s.split('_')
    elif re.search('[A-Z]+', s): # Case AbcDefGh or abcDefGh
        words = re.sub('([a-zA-Z])([A-Z])', lambda match: match.group(1).lower() + "_" + match.group(2).lower(), s).split('_')
    return words

def word_process(word):
    search_result = re.search("[0-9A-Za-z_]", word)
    if not search_result:
        return ""
    word = word[search_result.start():]
    while (len(word) > 0) and (not re.match("[0-9A-Za-z_]", word[-1:])):
        word = word[:-1]
    return word

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
    if word[:2] == '0x':
        return False
    word = re.sub("[^0-9A-Za-z_]", "", word)
    if(word.isdigit()):
        return False
    if(len(word) <= 2):
        return False
    return True

def analyse_project(project_name, crawler_mode=True):
    recrawler_mode = current_app.config['RECRAWLER_MODE']

    local_data_path = current_app.config['LOCAL_DATA_PATH']

    load_language_data(current_app.config['LANGUAGE_DATA_PATH'])

    repo_info = get_repo_info(local_data_path + "/" + project_name)

    if FLAGS_APP_MODE:
        # Load project into database.
        Project(
            project_name 		= project_name,
            language 			= repo_info["language"],
            fork_number 		= repo_info["forks"],
            description         = str(repo_info["description"]),
            analyser_progress   = "0%"
        ).save();

    forks_info = get_forks_info_dict(local_data_path + "/" + project_name)

    # forks = get_forks_list(main_path)
    # forks.sort(key=lambda x: x[1], reverse=True) # sort fork by last committed time

    print("-----start analysing for %s-----" % project_name)
    forks_number = len(forks_info)
    forks_count = 0
    for author in forks_info:
        forks_count += 1
        Project.objects(project_name = project_name).update(analyser_progress = "%d%%" % (100 * forks_count / forks_number))

        fork_name = forks_info[author]["full_name"]
        created_time = forks_info[author]["created_at"]
        last_committed_time = forks_info[author]["pushed_at"]
        # Ignore the fork if it doesn't have commits after fork.
        if last_committed_time <= created_time:
            continue
        # Load the result in local file.
        result_path = local_data_path + "/" + project_name + '/' + author + '/result.json'
        if (not recrawler_mode) and (os.path.exists(result_path)):
            with open(result_path) as read_file:
                compare_result = json.load(read_file)
        else:
            if crawler_mode:
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

        # Output & Save the changed file list of this fork.
        all_tokens = []
        all_stemmed_tokens = []
        file_list = []

        for file in compare_result["file_list"]:
            file_name = file["file_full_name"]
            file_suffix = file["file_suffix"]
            diff_link = file["diff_link"]
            changed_code = file["changed_code"]
            changed_line = file["changed_line"]
            common_tokens = []
            common_stemmed_tokens = []

            # Add files into fork's changed file list.
            file_list.append(file_name)

            # Check the language depend on the file suffix.
            file_language = ""
            for language in language_list:
                if(file_suffix in language_file_suffix[language]):
                    file_language = language
            if file_language:
                # process on changed code
                # get the tokens from changed code
                added_code = " ".join(filter(lambda x: (x) and (x[0] == '+'), changed_code.splitlines()))

                raw_tokens = nltk.word_tokenize(added_code)
                origin_tokens = [word_process(x) for x in raw_tokens]
                tokens = origin_tokens
                tokens = list(itertools.chain(*[word_split_by_char(token) for token in origin_tokens]))
                # tokens.extend(list(itertools.chain(*[word_split_by_char(token) for token in origin_tokens]))) # Keep original tokens
                
                #tokens = sum([word_split_by_char(token) for token in origin_tokens], origin_tokens)
                tokens = [x.lower() for x in tokens]
                tokens = filter(word_filter, tokens)
                tokens = filter(lambda x: x not in language_stop_words[file_language], tokens)
                tokens = list(tokens)
                stemmed_tokens = [PorterStemmer().stem(word) for word in tokens] # do stem on the tokens

                for x in tokens:
                    all_tokens.append(x)
                for x in stemmed_tokens:
                    all_stemmed_tokens.append(x)

                common_tokens = [x[0] for x in Counter(tokens).most_common(100)]
                common_stemmed_tokens = [x[0] for x in Counter(stemmed_tokens).most_common(100)]
                # load current file's name, key words to fork.
            else:
                file_language = "Unsupported"
            
            if FLAGS_APP_MODE:
                # Load changed files into database.
                ChangedFile(
                    full_name = project_name + '/' + fork_name + '/' + file_name,
                    file_name = file_name,
                    fork_name = fork_name,
                    project_name = project_name,
                    file_language = file_language,
                    file_suffix = file_suffix,
                    diff_link = diff_link,
                    # changed_code = file["changed_code"],
                    changed_line_number = changed_line,
                    key_words = common_tokens,
                    key_stemmed_words = common_stemmed_tokens,
                    # variable 
                    # class_name 
                    # function_name 
                ).save()

        # sorted_key_words = sorted(key_words.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        
        if FLAGS_APP_MODE:
            key_words = [x[0] for x in Counter(all_tokens).most_common(100)]
            key_stemmed_words = [x[0] for x in Counter(all_stemmed_tokens).most_common(100)]
            # Load forks into database.
            ProjectFork(
                full_name = project_name + '/' + fork_name,
                fork_name = fork_name,
                project_name = project_name,
                total_changed_file_number = compare_result["changed_file_number"],
                total_changed_line_number = compare_result["changed_line"],
                last_committed_time = datetime.datetime.strptime(last_committed_time, "%Y-%m-%dT%H:%M:%SZ"),
                created_time = datetime.datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%SZ"),
                file_list = file_list,
                key_words = key_words,
                key_stemmed_words = key_stemmed_words
            ).save();
    print("-----finish analysing for %s-----" % project_name)

"""
if __name__ == '__main__':
    print("Input the project name")
    project_name = raw_input().strip()
    analyse_project(project_name)
"""