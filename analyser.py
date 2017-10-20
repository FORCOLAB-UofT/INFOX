import os
import json
import compare_changes_crawler
from collections import Counter
import ConfigParser

result_file = './data/result.txt'

def get_repo_info(main_path):
    print '---------------------------------------'
    with open(main_path + '/repo_info.json') as read_file:
        repo_info = json.load(read_file)
        for type in ["language", "description", "forks"]:
            out_result = type + " : " + str(repo_info[type]) + "\n"
            print out_result
            with open(result_file, 'a') as write_file:
                write_file.write(out_result)

def get_forks_info_dict(main_path):
    print '---------------------------------------'
    forks_info = {}
    with open(main_path + '/forks.json') as read_file:
        forks_list = json.load(read_file)
        for fork in forks_list:
            fork_name = fork["full_name"].split('/')[0]
            forks_info[fork_name] = fork
    return forks_info

def get_forks_list(main_path):
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
    word = word.replace(',','').replace('+','').replace('-','').replace('0x','')
    if(word.isdigit()):
        return False
    if(len(word) <= 2):
        return False
    return True

def main():
    conf = ConfigParser.ConfigParser()
    conf.read('./config.conf')
    main_path = './tmp/%s_%s' % (conf.get("repo_info", "owner"), conf.get("repo_info", "repo"))

    get_repo_info(main_path)

    forks_info = get_forks_info_dict(main_path)

    forks = get_forks_list(main_path)

    forks.sort(key=lambda x: x[1], reverse=True) # sort fork by last committed time

    print "---------------------------------------"
    for (author, last_committed_time) in forks:
        created_time = forks_info[author]["created_at"]
        forks_full_name = forks_info[author]["full_name"]
        if last_committed_time > created_time:
            result_path = main_path + '/' + author + '/result.json'
            if os.path.exists(result_path):
                with open(result_path) as read_file:
                    compare_result = json.load(read_file)
            else:
                compare_result = compare_changes_crawler.compare(forks_full_name)
                with open(result_path, 'w') as write_file:
                   write_file.write(json.dumps(compare_result))
                # continue

            out_result = "fork_author: %18s, last committed time : %15s, " \
                         "created time: %15s, changed file: %3d, changed code line: %4d\n" % \
                         (author, last_committed_time, created_time, \
                          compare_result["changed_file_number"], \
                          compare_result["changed_line"])

            print out_result.strip()
            for file in compare_result["file_list"]:
                print file["file_full_name"] , ":", Counter(filter(word_filter, file["stemmed_tokens"])).most_common(10)
            print ""

            with open(result_file, 'a') as write_file:
                 write_file.write(out_result)

if __name__ == '__main__':
    main()
