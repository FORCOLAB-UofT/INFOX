import os
import json
import compare_changes_crawler
from collections import Counter
import ConfigParser
import codecs

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
    print '---------------------------------------'
    forks_info = {}
    with open(main_path + '/forks.json') as read_file:
        forks_list = json.load(read_file)
        for fork in forks_list:
            fork_name = fork["full_name"].split('/')[0]
            forks_info[fork_name] = fork
    return forks_info


def get_forks_list(main_path):
    """ Get the list of forks and it's last committed time.

    Args:
        main_path: the file store location.
    Return:
        A list of tuple of fork's full name and last committed time.
    """
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


def word_filter(word):
    """ The filter used for deleting the noisy words in changed code.
    Here is the method:
        1. Delete ',', '+', '-', '0x' 
        2. the length should large than 2.
    Args:
        word
    Return:
        True for not filtering, False for filtering.
    """
    word = word.replace(',','').replace('+','').replace('-','').replace('0x','')
    if(word.isdigit()):
        return False
    if(len(word) <= 2):
        return False
    return True

def main():
    # Load the config.
    conf = ConfigParser.ConfigParser()
    conf.read('./config.conf')
    main_path = './%s/%s_%s' % (conf.get("location", "save_path"),
                                conf.get("repo_info", "owner"),
                                conf.get("repo_info", "repo"))
    result_file = conf.get("location", "result_file") # the file for overview of all the forks.

    repo_info = get_repo_info(main_path)

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


    forks_info = get_forks_info_dict(main_path)

    forks = get_forks_list(main_path)

    # sort fork by last committed time
    forks.sort(key=lambda x: x[1], reverse=True)

    print "---------------------------------------"
    for (author, last_committed_time) in forks:
        created_time = forks_info[author]["created_at"]
        forks_full_name = forks_info[author]["full_name"]
        # Ignore the fork if it doesn't have commits after fork.
        if last_committed_time <= created_time:
            continue
        # Load the result in local file.
        result_path = main_path + '/' + author + '/result.json'
        if os.path.exists(result_path):
            with open(result_path) as read_file:
                compare_result = json.load(read_file)
        else:
            # If the compare result is not crawled, start to crawl.
            compare_result = compare_changes_crawler.compare(forks_full_name)
            with open(result_path, 'w') as write_file:
               write_file.write(json.dumps(compare_result))
            #continue

        # Ignore the fork if it is not changed.
        if compare_result["changed_line"] == 0:
            continue

        # Output & Save the overview of this fork.
        out_result = ("fork_author: %18s, last committed time : %15s, "
                      "created time: %15s, changed file: %3d, changed code line: %4d\n" %
                      (author, last_committed_time, created_time,
                       compare_result["changed_file_number"],
                       compare_result["changed_line"]))
        print out_result.strip()
        with codecs.open(result_file, 'a', 'utf-8') as write_file:
            write_file.write(out_result)

        # Output & Save the changed file list of this fork.
        for file in compare_result["file_list"]:
            common_tokens = Counter(filter(word_filter, file["tokens"])).most_common(10)
            common_stemmed_tokens = Counter(filter(word_filter, file["stemmed_tokens"])).most_common(10)
            print file["file_full_name"] , ":", common_tokens
            with codecs.open(result_file, 'a', 'utf-8') as write_file:
                write_file.write(file["file_full_name"] + ":\n")
                write_file.write('%35s' % 'common tokens: ')
                write_file.write(json.dumps(common_tokens))
                write_file.write('\n')
                write_file.write('%35s' % 'common tokens after stemming: ')
                write_file.write(json.dumps(common_stemmed_tokens))
                write_file.write('\n')
                write_file.write('\n')
        print ""

if __name__ == '__main__':
    main()
