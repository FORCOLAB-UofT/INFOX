import os
import json
import datetime
from flask import current_app

from . import compare_changes_crawler
from . import source_code_analyser
from .util import word_extractor
from .util import localfile_tool
from .util import language_tool
from .clone_crawler import CloneCrawler
from ..models import *

DATABASE_UPDATE_MODE=True

class ForkAnalyser:
    def __init__(self, project_name, author, fork_info, code_clone_crawler):
        self.project_name = project_name
        self.author = author
        self.fork_name = fork_info["full_name"]
        self.created_time = fork_info["created_at"]
        self.last_committed_time = fork_info["pushed_at"]
        self.code_clone_crawler = code_clone_crawler
        self.diff_result_path = current_app.config['LOCAL_DATA_PATH'] + "/" + self.project_name + '/' + self.author + '/diff_result.json'
        self.all_tokens = []
        # self.all_stemmed_tokens = []
        self.all_lemmatize_tokens = []
        self.file_list = []
    
    def get_tf_idf(self, tokens, top_number, list_option = True):
        tf_idf_dict = self.code_clone_crawler.calc_key_words_tfidf(word_extractor.get_counter(tokens))
        result = [(x, y) for x, y in sorted(tf_idf_dict.items(), key=lambda x: x[1], reverse=True)][:top_number]
        if list_option:
            return [x for x, y in result]
        else:
            return dict(result)

    def file_analyse(self, file):
        file_name = file["file_full_name"]
        file_suffix = file["file_suffix"]
        diff_link = file["diff_link"]
        changed_code = file["changed_code"]
        changed_line = file["changed_line"]
        common_tokens = []
        common_stemmed_tokens = []

        # Add files into fork's changed file list.
        self.file_list.append(file_name)

        # process on changed code
        # get the tokens from changed code
        added_code = " ".join(filter(lambda x: (x) and (x[0] == '+'), changed_code.splitlines()))
        # delete_code = " ".join(filter(lambda x: (x) and (x[0] == '-'), changed_code.splitlines()))

        tokens = word_extractor.get_words_from_text(file_name, added_code)
        lemmatize_tokens = word_extractor.lemmatize_process(tokens)
        # stemmed_tokens = word_extractor.stem_process(tokens)

        if DATABASE_UPDATE_MODE:
            # Load changed files into database.
            ChangedFile(
                full_name=self.project_name + '/' + self.fork_name + '/' + file_name,
                file_name=file_name,
                fork_name=self.fork_name,
                project_name=self.project_name,
                diff_link=diff_link,
                # changed_code=changed_code,
                changed_line_number=changed_line,
                key_words=word_extractor.get_top_words(tokens, 100),
                key_words_dict=word_extractor.get_top_words(tokens, 100, False),
                key_words_tfidf=self.get_tf_idf(tokens, 100),
                key_words_tf_idf_dict=self.get_tf_idf(tokens, 100, False),
                key_words_lemmatize_tfidf=self.get_tf_idf(lemmatize_tokens, 100),
                key_words_lemmatize_tfidf_dict=self.get_tf_idf(lemmatize_tokens, 100, False),
                # key_stemmed_words=word_extractor.get_top_words(stemmed_tokens, 100),
                # key_stemmed_words_dict=word_extractor.get_top_words(stemmed_tokens, 100, False),
            ).save()

        # Load current file's key words to fork.
        for x in tokens:
            self.all_tokens.append(x)
        for x in lemmatize_tokens:
            self.all_lemmatize_tokens.append(x)
        # for x in stemmed_tokens:
        #     self.all_stemmed_tokens.append(x)

    def work(self):
        # Ignore the fork if it doesn't have commits after fork.
        if self.last_committed_time <= self.created_time:
            return

        if (not current_app.config['RECRAWLER_MODE']) and (os.path.exists(self.diff_result_path)):
            with open(self.diff_result_path) as read_file:
                compare_result = json.load(read_file)
        else:
            # If the compare result is not crawled, start to crawl.
            try:
                compare_result = compare_changes_crawler.fetch_compare_page(self.fork_name)
            except:
                return
            if compare_result is not None:
                localfile_tool.write_to_file(self.diff_result_path, compare_result)
        
        for file in compare_result["file_list"]:
            self.file_analyse(file)

        try:
            tmp = source_code_analyser.get_info_from_fork_changed_code(self.fork_name)
            changed_code_name_list = tmp['name_list']
            changed_code_func_list = tmp['func_list']
        except:
            changed_code_name_list = []
            changed_code_func_list = []
        # print(word_extractor.get_top_words(changed_code_name_list, 10))
        
        if DATABASE_UPDATE_MODE:
            # Update forks into database.
            ProjectFork(
                full_name=self.project_name + '/' + self.fork_name,
                fork_name=self.fork_name,
                project_name=self.project_name,
                total_changed_file_number=compare_result["changed_file_number"],
                total_changed_line_number=compare_result["changed_line"],
                total_commit_number=len(compare_result["commit_list"]),
                commit_list=compare_result["commit_list"],
                last_committed_time=datetime.datetime.strptime(self.last_committed_time, "%Y-%m-%dT%H:%M:%SZ"),
                created_time=datetime.datetime.strptime(self.created_time, "%Y-%m-%dT%H:%M:%SZ"),
                file_list=self.file_list,
                key_words=word_extractor.get_top_words(self.all_tokens, 100),
                key_words_dict=word_extractor.get_top_words(self.all_tokens, 100, False),
                key_words_tfidf=self.get_tf_idf(self.all_tokens, 100),
                key_words_tf_idf_dict=self.get_tf_idf(self.all_tokens, 100, False),
                key_words_lemmatize_tfidf=self.get_tf_idf(self.all_lemmatize_tokens, 100),
                key_words_lemmatize_tfidf_dict=self.get_tf_idf(self.all_lemmatize_tokens, 100, False),
                variable=word_extractor.get_top_words(changed_code_name_list, 100),
                function_name=word_extractor.get_top_words(changed_code_func_list, 100),
                # key_stemmed_words=word_extractor.get_top_words(self.all_stemmed_tokens, 100),
                # key_stemmed_words_dict=word_extractor.get_top_words(self.all_stemmed_tokens, 100, False),
            ).save()

def update_progress(project_name, analyser_progress):
    Project.objects(project_name=project_name).update(analyser_progress=analyser_progress)

def analyse_project(project_name, repo_info, forks_info):
    if DATABASE_UPDATE_MODE:
        # Load project into database.
        Project(
            project_name=project_name,
            language=repo_info["language"],
            fork_number=repo_info["forks"],
            description=str(repo_info["description"]),
            analyser_progress="0%"
        ).save()

    forks_number = len(forks_info)
    forks_count = 0
    code_clone_crawler = CloneCrawler(project_name)
    for fork in forks_info:
        forks_count += 1
        update_progress(project_name, "%d%%" % (100 * forks_count / forks_number))
        author = fork["owner"]["login"]
        ForkAnalyser(project_name, author, fork, code_clone_crawler).work()


