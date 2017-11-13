# -*- coding: utf-8 -*- 

import os
import codecs
import math
from .util import word_extractor
from .util import language_tool

class CloneCrawler:
    doc_sets = []
    def __init__(self, project_name):
        self.project_name = project_name
        self.doc_sets = []
        self.get_doc_sets()

    def get_doc_sets(self):
        folder = '%s/%s/source_code' % ('/Users/fancycoder/infox_data/result', self.project_name)
        if not os.path.exists(folder):
            os.system('git clone https://github.com/%s.git %s' % (self.project_name.replace('_','/'), folder))
        
        # file_lists = []
        suceessful_file_number = 0
        for (fpath, dirs, fs) in os.walk(folder):
            for file_name in fs:
                file_full_name = os.path.join(fpath, file_name)
                if language_tool.is_text(file_name):
                    # file_lists.append(file_full_name)
                    with codecs.open(file_full_name, 'rU', 'utf-8') as f:
                        try:
                            content = f.read()
                            #print(content)
                            tokens = set(word_extractor.get_words_from_text(file_name, content))
                            self.doc_sets.append(tokens)
                            suceessful_file_number += 1
                        except:
                            pass
        print('%s suceessful_file_number: %d' % (self.project_name, suceessful_file_number))

    def calc_key_words_tfidf(self, word_counter):
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
            IDF = math.log(1.0 *  doc_num / (number + 1))
            TFIDF[word] = TF * IDF
        # print("finish calc!")
        return TFIDF

