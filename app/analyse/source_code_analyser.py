import os
import requests
import re
import xml.etree.ElementTree as ET
import platform

from flask import current_app
from .util import language_tool

def get_fork_changed_code_name_list(project_full_name):
    url = 'https://github.com/%s/compare' % project_full_name
    # It will jump to https://github.com/author/repo/compare/version...author:repo
    url = requests.get(url).url
    url += '.patch'
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        content = r.text
    else:
        print("error on get diff for %s!" % project_full_name)
        return None
    
    diff_list = content.split('diff --git')

    all_added_code = []
    all_name_list = []
    for diff in diff_list[1:]:
        try:
            file_full_name = re.findall('a\/.*? b\/(.*?)\n', diff)[0]
        except:
            print('error on fetch', project_full_name)
            continue

        file_name, file_suffix = os.path.splitext(file_full_name)
        st = re.search('@@.*?-.*?\+.*?@@', diff)
        if st is None:
            continue
        parts = re.split('@@.*?-.*?\+.*?@@', diff[st.start():])

        start_with_plus_regex = re.compile('^\++')
        if file_suffix in ['.java','.cpp','.cc','.c','.h','.cs']:
            added_code = ''
            for part in parts:
                lines_of_code = filter(lambda x: (x) and (x[0] == '+'), part.splitlines())
                added_code+="\n".join([start_with_plus_regex.sub('', x) for x in lines_of_code])
            file_path = '%s/added_code/%s/%s' % (current_app.config['LOCAL_DATA_PATH'], project_full_name, file_full_name)
            file_dir = os.path.dirname(file_path)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            with open(file_path, 'w') as f:
                f.write(added_code)

            if platform.system() == 'Darwin':
                srcML_name = 'srcML'
            elif platform.system() == 'Linux':
                srcML_name = 'src2srcml'
        
            srcML_result = os.popen('%s %s' % (srcML_name, file_path), 'r').read()
            name_list = filter(lambda x: (x) and (len(x) > 2), [x.text for x in ET.fromstring(srcML_result).iter(tag='{http://www.srcML.org/srcML/src}name')])
            name_list = filter(lambda x: x not in language_tool.get_language_stop_words(language_tool.get_language(file_full_name)), name_list)
            all_added_code.extend(added_code)
            all_name_list.extend(name_list)

    return all_name_list


