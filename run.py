import ConfigParser
import crawler
import analyser

conf = ConfigParser.ConfigParser()
conf.read('./config.conf')
owner = conf.get("repo_info", "owner")
repo = conf.get("repo_info", "repo")
print "Input repo's owner & repo's name (like FancyCoder0/INFOX): "
try:
    owner, repo = raw_input().strip().split('/')
except:
    print "Use default: %s/%s" % (owner, repo)
    pass

conf.set("repo_info", "owner", owner)
conf.set("repo_info", "repo", repo)
with open("config.conf", "w") as fp:
    conf.write(fp)

crawler.author_name = owner
crawler.project_name = repo

print "Input your personal access token:"
access_token = raw_input().strip()
crawler.access_token = access_token

print "Set config successfully!"

print "Start running crawler!"
crawler.main()
print "Finish runningcrawler!"

print "Start running analyser"
analyser.main()
print "Finish running analyser!"