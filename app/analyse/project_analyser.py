import os
import json
import datetime
from flask import current_app

from . import compare_changes_crawler
from .util import word_extractor
from .util import localfile_tool
from .util import language_tool
from .clone_crawler import CloneCrawler
from ..models import Project, ProjectFork, ChangedFile

class ForkAnalyser:
    def __init__(self, project_name, author, fork_info, code_clone_crawler):
        self.project_name = project_name
        self.author = author
        self.fork_name = fork_info["full_name"]
        self.created_time = fork_info["created_at"]
        self.last_committed_time = fork_info["pushed_at"]
        self.code_clone_crawler = code_clone_crawler
        # Load the result in local file.
        self.result_path = current_app.config['LOCAL_DATA_PATH'] + "/" + self.project_name + '/' + self.author + '/result.json'
        
        self.all_tokens = []
        self.all_stemmed_tokens = []
        self.file_list = []
        
    def work(self):
        # Ignore the fork if it doesn't have commits after fork.
        if self.last_committed_time <= self.created_time:
            return
        
        if (not current_app.config['RECRAWLER_MODE']) and (os.path.exists(self.result_path)):
            with open(self.result_path) as read_file:
                compare_result = json.load(read_file)
        else:
            # If the compare result is not crawled, start to crawl.
            compare_result = compare_changes_crawler.compare(self.fork_name)
            if(compare_result["changed_file_number"] == -1):
                return
            localfile_tool.write_to_file(self.result_path, compare_result)

        # Ignore the fork if it is not changed.
        if compare_result["changed_line"] == 0:
            return

        for file in compare_result["file_list"]:
            self.file_analyse(file)

        tf_idf_dict = self.code_clone_crawler.calc_key_words_tfidf(word_extractor.get_counter(self.all_tokens)) # change to fork_name
        
        # Load forks into database.
        ProjectFork(
            full_name = self.project_name + '/' + self.fork_name,
            fork_name = self.fork_name,
            project_name = self.project_name,
            total_changed_file_number = compare_result["changed_file_number"],
            total_changed_line_number = compare_result["changed_line"],
            last_committed_time = datetime.datetime.strptime(self.last_committed_time, "%Y-%m-%dT%H:%M:%SZ"),
            created_time = datetime.datetime.strptime(self.created_time, "%Y-%m-%dT%H:%M:%SZ"),
            file_list = self.file_list,
            key_words = word_extractor.get_top_words_list(self.all_tokens, 100),
            key_stemmed_words = word_extractor.get_top_words_list(self.all_stemmed_tokens, 100),
            key_words_counter_dict = dict((x, y) for x, y in word_extractor.get_top_words_tuple(self.all_tokens, 100)),
            key_words_by_tfidf = [x[0] for x in sorted(tf_idf_dict.items(), key = lambda x: x[1], reverse=True)[:100]],
            key_words_tf_idf_dict = dict((x, y) for x, y in sorted(tf_idf_dict.items(), key = lambda x: x[1], reverse=True)[:100]),
        ).save();

    def file_analyse(self, file):
        file_name = file["file_full_name"]
        file_suffix = file["file_suffix"]
        try:
            diff_link = file["diff_link"]
        except:
            diff_link = ""
        changed_code = file["changed_code"]
        changed_line = file["changed_line"]
        common_tokens = []
        common_stemmed_tokens = []

        # Add files into fork's changed file list.
        self.file_list.append(file_name)

        # process on changed code
        # get the tokens from changed code
        added_code = " ".join(filter(lambda x: (x) and (x[0] == '+'), changed_code.splitlines()))

        tokens = word_extractor.get_words_from_text(file_name, added_code)
        stemmed_tokens = word_extractor.stem_process(tokens)

        common_tokens = word_extractor.get_top_words_list(tokens, 100)
        common_stemmed_tokens = word_extractor.get_top_words_list(stemmed_tokens, 100)

        # Load current file's key words to fork.
        for x in tokens:
            self.all_tokens.append(x)
        for x in stemmed_tokens:
            self.all_stemmed_tokens.append(x)
        # Load changed files into database.
        ChangedFile(
            full_name = self.project_name + '/' + self.fork_name + '/' + file_name,
            file_name = file_name,
            fork_name = self.fork_name,
            project_name = self.project_name,
            diff_link = diff_link,
            # changed_code = file["changed_code"],
            changed_line_number = changed_line,
            key_words = common_tokens,
            key_stemmed_words = common_stemmed_tokens,
            # variable 
            # class_name 
            # function_name 
        ).save()

def update_progress(project_name, analyser_progress):
    Project.objects(project_name = project_name).update(analyser_progress = analyser_progress)

def analyse_project(project_name):
    repo_info = localfile_tool.get_repo_info(current_app.config['LOCAL_DATA_PATH'] + "/" + project_name)
    forks_info = localfile_tool.get_forks_info_dict(current_app.config['LOCAL_DATA_PATH'] + "/" + project_name)
    # forks = localfile_tool.get_forks_list(main_path)
    # forks.sort(key=lambda x: x[1], reverse=True) # sort fork by last committed time

    # Load project into database.
    Project(
        project_name 		= project_name,
        language 			= repo_info["language"],
        fork_number 		= repo_info["forks"],
        description         = str(repo_info["description"]),
        analyser_progress   = "0%"
    ).save();

    print("-----start analysing for %s-----" % project_name)
    forks_number = len(forks_info)
    forks_count = 0
    code_clone_crawler = CloneCrawler(project_name)
    for author in forks_info:
        forks_count += 1
        update_progress(project_name, "%d%%" % (100 * forks_count / forks_number))
    
        ForkAnalyser(project_name, author, forks_info[author], code_clone_crawler).work()
        
    print("-----finish analysing for %s-----" % project_name)
