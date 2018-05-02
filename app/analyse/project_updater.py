import os
import json
from collections import OrderedDict
from datetime import datetime
from flask import current_app

from . import compare_changes_crawler
from . import source_code_analyser
from .util import word_extractor
from .util import localfile_tool
from .clone_crawler import CloneCrawler
from ..models import *

DATABASE_UPDATE_MODE=True

class ForkUpdater:
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
        added_code = file["added_code"]
        changed_line = file["added_line"]

        # process on changed code, get the tokens from changed code
        tokens = word_extractor.get_words_from_file(file_name, added_code)
        # lemmatize_tokens = word_extractor.lemmatize_process(tokens)
        # stemmed_tokens = word_extractor.stem_process(tokens)

        # Load changed files into database.
        ChangedFile(
            full_name=self.project_name + '/' + self.fork_name + '/' + file_name,
            file_name=file_name,
            fork_name=self.fork_name,
            project_name=self.project_name,
            diff_link=diff_link,
            # changed_code=changed_code,
            changed_line_number=changed_line,
            # key_words=word_extractor.get_top_words(tokens, 10),
            # key_words_dict=word_extractor.get_top_words(tokens, 10, False),
            # key_words_tfidf=self.get_tf_idf(tokens, 10),
            # key_words_tf_idf_dict=self.get_tf_idf(tokens, 10, False),
            # key_words_lemmatize_tfidf=self.get_tf_idf(lemmatize_tokens, 10),
            # key_words_lemmatize_tfidf_dict=self.get_tf_idf(lemmatize_tokens, 10, False),
            # key_stemmed_words=word_extractor.get_top_words(stemmed_tokens, 10),
            # key_stemmed_words_dict=word_extractor.get_top_words(stemmed_tokens, 10, False),
        ).save()

        # Load current file's key words to fork.
        for x in tokens:
            self.all_tokens.append(x)
        # for x in lemmatize_tokens:
        #     self.all_lemmatize_tokens.append(x)
        # for x in stemmed_tokens:
        #     self.all_stemmed_tokens.append(x)

    def work(self):
        # Ignore the fork if it doesn't have commits after fork.
        if self.last_committed_time <= self.created_time:
            return
        
        last_update = ProjectFork.objects(full_name=self.project_name + '/' + self.fork_name).first()

        if (not current_app.config['FORCED_UPDATING']) and (last_update is not None) and (datetime.strptime(self.last_committed_time, "%Y-%m-%dT%H:%M:%SZ") == last_update.last_committed_time) \
        and (last_update.total_changed_line_number != -1):
            return

        # Update time first.
        ProjectFork(
            full_name=self.project_name + '/' + self.fork_name,
            fork_name=self.fork_name,
            project_name=self.project_name,
            last_committed_time=datetime.strptime(self.last_committed_time, "%Y-%m-%dT%H:%M:%SZ"),
            created_time=datetime.strptime(self.created_time, "%Y-%m-%dT%H:%M:%SZ")).save()

        if current_app.config['USE_LOCAL_FORK_INFO']:
            # load from local.
            if os.path.exists(self.diff_result_path):
                with open(self.diff_result_path) as read_file:
                    compare_result = json.load(read_file)
            else:
                # local file not exist
                return
        else:
            # If the compare result is not crawled, start to crawl.
            compare_result = compare_changes_crawler.fetch_compare_page(self.fork_name)
            if compare_result is not None:
                localfile_tool.write_to_file(self.diff_result_path, compare_result)

        for file in compare_result["file_list"]:
            try:
                self.file_analyse(file)
            except:
                pass
        try:
            tmp = source_code_analyser.get_info_from_fork_changed_code(self.fork_name)
            changed_code_name_list = tmp['name_list']
            changed_code_func_list = tmp['func_list']
        except:
            changed_code_name_list = []
            changed_code_func_list = []
        # print(word_extractor.get_top_words(changed_code_name_list, 10))
        

        # Update forks in database.
        full_name = self.project_name + '/' + self.fork_name

        file_distinct = list(OrderedDict.fromkeys([x["file_full_name"] for x in compare_result["file_list"]]))
        
        self.all_lemmatize_tokens = word_extractor.lemmatize_process(self.all_tokens)

        project_name_stop_words = (self.project_name + '/' + self.fork_name).split('/')
        self.all_lemmatize_tokens = list(filter(lambda x: x not in project_name_stop_words, self.all_lemmatize_tokens))

        # Update forks into database.
        ProjectFork(
            full_name=self.project_name + '/' + self.fork_name,
            fork_name=self.fork_name,
            project_name=self.project_name,
            total_changed_file_number=len(file_distinct),
            total_changed_line_number=sum([x["added_line"] for x in compare_result["file_list"]]),
            total_commit_number=len(compare_result["commit_list"]),
            commit_list=compare_result["commit_list"],
            last_committed_time=datetime.strptime(self.last_committed_time, "%Y-%m-%dT%H:%M:%SZ"),
            created_time=datetime.strptime(self.created_time, "%Y-%m-%dT%H:%M:%SZ"),
            file_list=file_distinct,
            key_words=word_extractor.get_top_words(self.all_tokens, 10),
            key_words_lemmatize_tfidf=self.get_tf_idf(self.all_lemmatize_tokens, 10),
            # key_words_dict=word_extractor.get_top_words(self.all_tokens, 10, False),
            # key_words_tfidf=self.get_tf_idf(self.all_tokens, 10),
            # key_words_tf_idf_dict=self.get_tf_idf(self.all_tokens, 10, False),
            # key_words_lemmatize_tfidf_dict=self.get_tf_idf(self.all_lemmatize_tokens, 10, False),
            variable=word_extractor.get_top_words(changed_code_name_list, 10),
            function_name=word_extractor.get_top_words(changed_code_func_list, 10),
            last_updated_time=datetime.utcnow(),
            # key_stemmed_words=word_extractor.get_top_words(self.all_stemmed_tokens, 10),
            # key_stemmed_words_dict=word_extractor.get_top_words(self.all_stemmed_tokens, 10, False),
        ).save()


def get_activate_fork_number(forks_info):
    number = 0
    for fork in forks_info:
        if fork["pushed_at"] > fork["created_at"]:
            number += 1
    return number

def project_init(project_name, repo_info):
    # Update project in database.
    Project(
        project_name=project_name,
        language=repo_info["language"],
        fork_number=repo_info["forks"],
        activate_fork_number=-1,
        description=str(repo_info["description"]),
        analyser_progress="0%",
    ).save()

def start_update(project_name, repo_info, forks_info):
    Project.objects(project_name=project_name).update(activate_fork_number=get_activate_fork_number(forks_info))

    forks_number = len(forks_info)
    forks_count = 0
    code_clone_crawler = CloneCrawler(project_name)
    for fork in forks_info:
        forks_count += 1
        try:
            ForkUpdater(project_name, fork["owner"]["login"], fork, code_clone_crawler).work()
        except Exception as inst:
            print(inst)
        finally:
            Project.objects(project_name=project_name).update(analyser_progress="%d%%" % (100 * forks_count / forks_number))
            Project.objects(project_name=project_name).update(last_updated_time=datetime.utcnow())
    Project.objects(project_name=project_name).update(analyser_progress="%d%%" % 100)

