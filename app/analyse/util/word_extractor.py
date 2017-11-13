import os
import re
import nltk
from nltk.stem.porter import PorterStemmer
from collections import Counter
import itertools

from . import language_tool

def word_split_by_char(s):
    words = []
    if '-' in s: # Case: ab-cd-ef
        words = s.split('-')
    elif '.' in s: # Case: ab.cd.ef
        words = s.split('.')
    elif '_' in s: # Case: ab_cd_ef
        words = s.split('_')
    elif '/' in s: # Case: ab/cd/ef
        words = s.split('/')
    elif re.search('[A-Z]+', s): # Case AbcDefGh or abcDefGh
        words = re.sub('([a-zA-Z])([A-Z])', lambda match: match.group(1).lower() + "_" + match.group(2).lower(), s).split('_')
    return words

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
    Return:
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

def stem_process(tokens):
    return [PorterStemmer().stem(word) for word in tokens] # do stem on the tokens

def get_words_from_text(file, text):
    if not language_tool.is_text(file):
        return []
    raw_tokens = nltk.word_tokenize(text)
    origin_tokens = [word_process(x) for x in raw_tokens]
    tokens = origin_tokens
    tokens = list(itertools.chain(*[word_split_by_char(token) for token in origin_tokens]))
    # tokens.extend(list(itertools.chain(*[word_split_by_char(token) for token in origin_tokens]))) # Keep original tokens
    
    #tokens = sum([word_split_by_char(token) for token in origin_tokens], origin_tokens)
    tokens = [x.lower() for x in tokens]
    tokens = filter(word_filter, tokens)
    tokens = filter(lambda x: x not in language_tool.get_language_stop_words(language_tool.get_language(file)), tokens)
    tokens = list(tokens)

    # stemmed_tokens = [PorterStemmer().stem(word) for word in tokens] # do stem on the tokens
    return tokens

def get_counter(tokens):
    return Counter(tokens)

def get_top_words_tuple(tokens, top_number):
    counter = get_counter(tokens)
    return counter.most_common(top_number)

def get_top_words_list(tokens, top_number):
    counter = get_counter(tokens)
    return [x[0] for x in counter.most_common(top_number)]
