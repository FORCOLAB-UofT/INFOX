import ConfigParser
import crawler

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

print "Input your personal access token:"
access_token = raw_input().strip()
if(len(access_token) != 40):
    access_token = ""
    print "Invaild access token!"

conf.set("repo_info", "owner", owner)
conf.set("repo_info", "repo", repo)
conf.set("token", "access_token", access_token)

with open("config.conf", "w") as fp:
    conf.write(fp)

print "Set config successfully!"

print "Start running crawler!"
crawler.main()
print "Finish runningcrawler!"
