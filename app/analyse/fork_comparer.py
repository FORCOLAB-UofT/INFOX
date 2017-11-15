from flask import current_app


def compare_on_files(fork1, fork2):
    common_path = set()

    f2_path_list = []
    for fork2_file_name in fork2.file_list:
        fork2_dirs = fork2_file_name.split('/')
        current_path = ""
        for d in fork2_dirs:
            current_path += '/' + d
            f2_path_list.append(current_path)

    for fork1_file_name in fork1.file_list:
        fork1_dirs = fork1_file_name.split('/')
        current_path = ""
        deepest_common_path = ""
        for d in fork1_dirs:
            current_path += '/' + d
            if current_path in f2_path_list:
                deepest_common_path = current_path
        if deepest_common_path:
            common_path.add(deepest_common_path)

    return list(common_path)


def compare_on_key_words(fork1, fork2):
    common_words = []
    for word in fork1.key_words:
        if word in fork2.key_words:
            common_words.append(word)
    return common_words
