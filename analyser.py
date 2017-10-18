import os
import json
import crawler
import compare_changes_crawler

def main():
    main_path = crawler.save_path % (crawler.author_name, crawler.project_name)
    print '---------------------------------------'
    with open(main_path + '/repo_info.json') as read_file:
        repo_info = json.load(read_file)
        print 'language: %s' % repo_info["language"]
        print 'description: %s' % repo_info["description"]
        print 'forks number: %d' % repo_info["forks"]

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

    forks.sort(key=lambda x: x[1]) # sort fork by last committed time

    print "---------------------------------------"
    for (author, last_committed_time) in forks:
        created_time = forks_info[author]["created_at"]
        forks_full_name = forks_info[author]["full_name"]
        if last_committed_time > created_time:
            compare_result = compare_changes_crawler.compare(forks_full_name)
            out_result = "fork_author: %20s, last committed time : %20s, " \
                         "created time: %20s, changed line: %d\n" % \
                         (author, last_committed_time, created_time, compare_result)
            print out_result
            with open('sorted_result.txt', 'a') as write_file:
                write_file.write(out_result)

if __name__ == '__main__':
    main()
