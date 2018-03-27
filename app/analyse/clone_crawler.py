# -*- coding: utf-8 -*-

import os
import codecs
import math

from flask import current_app
from .util import word_extractor
from .util import language_tool


class CloneCrawler:
    """ Clone Crawler.

    Attributes:
        project name
    """
    doc_sets = []

    def __init__(self, project_name):
        self.project_name = project_name
        self.doc_sets = []
        self.get_doc_sets()

    def get_doc_sets(self):
        """ Get all the text content.
        """
        folder = '%s/%s/source_code' % (
            current_app.config['LOCAL_DATA_PATH'], self.project_name)
        # TODO(luyao) Some problem. file may be update.
        if not os.path.exists(folder):
            os.system('git clone --depth=1 https://github.com/%s.git %s' %
                      (self.project_name.replace('_', '/'), folder))

        # file_lists = []
        suceessful_file_number = 0
        for (fpath, dirs, fs) in os.walk(folder):
            no_text_file_numer = 0
            for file_name in fs:
                file_full_name = os.path.join(fpath, file_name)
                if language_tool.is_text(file_name) and os.path.getsize(file_full_name) <= 1024 * 100:
                    # print(file_full_name)
                    # file_lists.append(file_full_name)
                    with codecs.open(file_full_name, 'rU', 'utf-8') as f:
                        try:
                            content = f.read()
                            # print(content)
                            tokens = set(word_extractor.get_words_from_file(
                                file_name, content))
                            self.doc_sets.append(tokens)
                            suceessful_file_number += 1
                        except:
                            pass
                    # print("finish")
                else:
                    no_text_file_numer+=1
                    if no_text_file_numer > 50:
                        break
        print('%s suceessful_file_number: %d' %
              (self.project_name, suceessful_file_number))

    def calc_key_words_tfidf(self, word_counter):
        """ Calculate the TF-IDF of the word_counter.
            Args:
                word_counter: a list of the word count tuple
                              Example: [('a',1), ('b',2)]
            Returns:
                A dict of the TF-IDF of each word.
                Example: { 'a': 0.1, 'b': 0.3 }
        """
        # print("calc tfidf for %s" % project_name)
        TFIDF = {}
        times_total = 0
        max_times = 0
        for word in word_counter:
            times_total += word_counter[word]
            max_times = max(max_times, word_counter[word])

        doc_num = len(self.doc_sets)
        for word in word_counter:
            TF = 1.0 * word_counter[word] / times_total
            # TF = 1.0 * times / max_times
            number = 0
            for i in range(doc_num):
                if word in self.doc_sets[i]:
                    number += 1
            if doc_num == 0:
                IDF = 1
            else:
                IDF = math.log(1.0 * doc_num / (number + 1))
            TFIDF[word] = TF * IDF
        # print("finish calc!")
        return TFIDF
