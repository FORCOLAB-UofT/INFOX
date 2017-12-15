from flask import current_app


def compare_on_files(fork1, fork2):
    """
        Args:
            fork1: ProjectFork
            fork2: ProjectFork
        Return:
            A list contains the common path of the two forks.
    """
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
    """
        Args:
            fork1: ProjectFork
            fork2: ProjectFork
        Return:
            A list contains the common key words of the two forks.       
    """
    common_words = []
    for word in fork1.key_words:
        if word in fork2.key_words:
            common_words.append(word)
    return common_words


def get_familiar_fork(fork_list, fork1):
    """
        Args:
            fork_list
            fork1
        Return:
            A list contains the similar forks with fork1 (Top 5)    
    """
    if (fork_list is None) or (fork1 is None):
        return None
    
    sort_list = {}
    for fork2 in fork_list:
        if fork2.full_name == fork1.full_name:
            continue
        n_common_words = len(compare_on_key_words(fork1, fork2))
        n_dep_commpn_files = 0
        commpn_files = compare_on_files(fork1, fork2)
        for file in commpn_files:
            n_dep_commpn_files += file.count('/')
        
        # print(n_common_words, n_dep_commpn_files)
        value = n_common_words + 5 * n_dep_commpn_files
        sort_list[fork2.fork_name] = value
     
    result = [x for x, y in sorted(sort_list.items(), key=lambda x: x[1], reverse=True)][:5]
    return result

