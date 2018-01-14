import os

FLAGS_load_language_data = False
language_list = []
language_file_suffix = {}
language_stop_words = {}
text_suffix = []
general_stopwords = []

language_data_path = os.path.dirname(os.path.realpath(__file__)) + '/data'


def init():
    """ Load the language data.
    """
    global FLAGS_load_language_data
    if FLAGS_load_language_data:
        return
    with open(language_data_path + '/text_suffix.txt') as read_file:
        for line in read_file.readlines():
            text_suffix.append(line.strip())

    with open(language_data_path + '/support_language.txt') as read_file:
        for line in read_file.readlines():
            if line:
                language = line.strip()
                language_list.append(language)
                language_file_suffix[language] = []
                language_stop_words[language] = []
                with open(language_data_path + '/' + language + '_suffix.txt') as f:
                    for line in f.readlines():
                        if line:
                            suffix = line.strip()
                            language_file_suffix[language].append(suffix)
                with open(language_data_path + '/' + language + '_stopwords.txt') as f:
                    for line in f.readlines():
                        if line:
                            word = line.strip()
                            language_stop_words[language].append(word)

    with open(language_data_path + '/general_stopwords.txt') as read_file:
        for line in read_file.readlines():
            if line:
                word = line.strip()
                general_stopwords.append(word)

    FLAGS_load_language_data = True


def get_language_stop_words(language):
    init()
    if language in language_stop_words:
        return language_stop_words[language]
    else:
        return []

def get_general_stopwords(language):
    init()
    return general_stopwords

def get_language_on_suffix(file_suffix):
    """ Get the language depend on the suffix.
        Args:
            suffix
        Returns:
            language

            example:
                cpp -> cpluscplus
    """
    init()
    # Check the language depend on the file suffix.
    file_language = ""
    for language in language_list:
        if (file_suffix in language_file_suffix[language]):
            file_language = language
    return file_language


def get_language(file):
    """ Get the language depend on the file name.
        Args:
            file name
        Returns:
            file language
            
            example: a.cpp -> cplusplus
    """
    file_name, file_suffix = os.path.splitext(file)
    return get_language_on_suffix(file_suffix)


def is_text(file):
    """ The file is text
        Args:
            file full name
        Returns:
            True/False
    """
    init()
    if '.' not in file:
        return False
    file_name, file_suffix = os.path.splitext(file)
    file_suffix = file_suffix.strip()
    if file_suffix in text_suffix:
        return True
    else:
        return False
