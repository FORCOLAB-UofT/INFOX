import os
import json
import crawler
import compare_changes_crawler

def main():
    crawler.author_name = 'Smoothieware'
    crawler.project_name = 'Smoothieware'

    main_path = crawler.save_path % (crawler.author_name, crawler.project_name)
    print '---------------------------------------'
    with open(main_path + '/repo_info.json') as read_file:
        repo_info = json.load(read_file)
        for type in ["language", "description", "forks"]:
            out_result = type + " : " + str(repo_info[type]) + "\n"
            print out_result
            with open('sorted_result.txt', 'a') as write_file:
                write_file.write(out_result)
    print '---------------------------------------'
    forks_info = {}
    with open(main_path + '/forks.json') as read_file:
        forks_list = json.load(read_file)
        for fork in forks_list:
            fork_name = fork["full_name"].split('/')[0]
            forks_info[fork_name] = fork

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
                    print "missing commit on %s" % dir

    forks.sort(key=lambda x: x[1], reverse=True) # sort fork by last committed time

    print "---------------------------------------"
    for (author, last_committed_time) in forks:
        created_time = forks_info[author]["created_at"]
        forks_full_name = forks_info[author]["full_name"]
        if last_committed_time > created_time:
            changed_file_number, total_changed_line = compare_changes_crawler.compare(forks_full_name)
            out_result = "fork_author: %15s, last committed time : %15s, " \
                         "created time: %15s, changed file: %6d, changed code line: %6d\n" % \
                         (author, last_committed_time, created_time, changed_file_number, total_changed_line)
            print out_result
            with open('sorted_result.txt', 'a') as write_file:
                write_file.write(out_result)

if __name__ == '__main__':
    main()
