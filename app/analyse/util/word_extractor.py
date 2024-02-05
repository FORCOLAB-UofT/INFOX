import os
import re
import nltk
import itertools
import time
from collections import Counter
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

from . import language_tool

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def word_split_by_char(s):
    """ split the word by some separators
        Args:
            Word
        Returns:
            List of the split words
    """
    old_words = []
    old_words.append(s)
    result = []
    while len(old_words) > 0:
        new_words = []
        for s in old_words:
            if '-' in s:  # Case: ab-cd-ef
                new_words+=s.split('-')
            elif '.' in s:  # Case: ab.cd.ef
                new_words+=s.split('.')
            elif '_' in s:  # Case: ab_cd_ef
                new_words+=s.split('_')
            elif '/' in s:  # Case: ab/cd/ef
                new_words+=s.split('/')
            elif '\\' in s: # Case: ab\cd\ef
                new_words+=s.split('\\')
            else:
                if re.search('[A-Z]+', s):  # Case AbcDefGh or abcDefGh
                    result+=re.sub('([a-zA-Z])([A-Z])', lambda match: match.group(1).lower() + "_" + match.group(2).lower(), s).split('_')
                result.append(s)
        old_words = new_words
    return result

def word_process(word):
    search_result = re.search("[0-9A-Za-z_]", word)
    if not search_result:
        return ""
    word = word[search_result.start():]
    while (len(word) > 0) and (not re.match("[0-9A-Za-z_]", word[-1:])):
        word = word[:-1]
    return word


def word_filter(word):
    """ The filter used for deleting the noisy words in changed code.
    Here is the method:
        1. Delete character except for digit, alphabet, '_'.
        2. the word shouldn't be all digit.
        3. the length should large than 2.
    Args:
        word
    Returns:
        True for not filtering, False for filtering.
    """
    if word[:2] == '0x':
        return False
    if '=' in word:
        return False
    if '/' in word:
        return False
    if '.' in word:
        return False
    if '$' in word:
        return False
    word = re.sub("[^0-9A-Za-z_]", "", word)
    if(word.isdigit()):
        return False
    if(len(word) <= 2):
        return False
    return True

"""
def stem_process(tokens):
    # Do stem on the tokens.
    for try_times in range(3):
        try:
            result = [stemmer.stem(word) for word in tokens]
            return result
        except:
            print('error on stem_process')
            time.sleep(5)
    return tokens
"""

def lemmatize_process(tokens):
    for try_times in range(3): # NLTK is not thread-safe, use simple retry to fix it.
        try:
            result = [lemmatizer.lemmatize(word) for word in tokens]
        except:
            print('error on lemmatize_process')
            time.sleep(5)
    return tokens

def move_other_char(text):
    return re.sub("[^0-9A-Za-z_]", "", text)

def get_words_from_file(file, text):
    """
        Args:
            file: file full name
            text: the raw text of the file
        Returns:
            A list of the tokens of the result of the participle. 
    """
    if file and (not language_tool.is_text(file)):
        return []
    if text is None:
        return []
    raw_tokens = nltk.word_tokenize(text)
    origin_tokens = [word_process(x) for x in raw_tokens]
    tokens = origin_tokens
    tokens = list(itertools.chain(*[word_split_by_char(token) for token in origin_tokens]))
    tokens.extend(list(itertools.chain(*[word_split_by_char(token) for token in origin_tokens]))) # Keep original tokens

    #tokens = sum([word_split_by_char(token) for token in origin_tokens], origin_tokens)
    tokens = [x.lower() for x in tokens]
    tokens = filter(word_filter, tokens)
    tokens = filter(lambda x: x not in language_tool.get_language_stop_words(
        language_tool.get_language(file)), tokens)
    tokens = filter(lambda x: x not in language_tool.get_general_stopwords(), tokens)
    tokens = list(tokens)

    # stemmed_tokens = [PorterStemmer().stem(word) for word in tokens] # do stem on the tokens
    return tokens

def get_words(text):
    return get_words_from_file('1.txt', text)

def get_counter(tokens):
    tokens = filter(lambda x: x is not None, tokens)
    return Counter(tokens)

def get_top_words(tokens, top_number, list_option = True):
    if tokens is None:
        return None
    counter = get_counter(tokens).most_common(top_number)
    if list_option:
        return [x for x, y in counter]
    else:
        return dict([(x,y) for x, y in counter])

# just for test
def get_top_words_from_text(text, top_number=10):
    return get_top_words(get_words(text), top_number)
