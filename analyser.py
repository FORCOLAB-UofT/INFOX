import os
import json

save_path = './tmp/Smoothieware_Smoothieware'

with open(save_path + '/repo_info.json') as f:
    repo_info = json.load(f)
    print ('language: %s' % repo_info["language"])
    print ('description: %s' % repo_info["description"])
    print ('forks number: %d' % repo_info["forks"])

forks = []
dir_list = os.listdir(save_path)
for dir in dir_list:
    if os.path.isdir(save_path + '/' + dir):
        with open(save_path + '/' + dir + '/commits.json') as f:
            commits = json.load(f)
            date = commits[0]["commit"]["committer"]["date"]
            forks.append((dir, date))

forks.sort(key = lambda x:x[1]) # sort fork by last committed time

for (fork, commit_time) in forks:
    print ("fork_author: %20s, last committed time : %20s" % (fork, commit_time))
