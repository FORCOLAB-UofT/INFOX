"""
import os
import requests
import re
import xml.etree.ElementTree as ET
import platform

from flask import current_app
from .util import language_tool
"""

def get_info_from_fork_changed_code(project_full_name):
    all_name_list = []
    all_func_list = []
    
    """
    url = 'https://github.com/%s/compare' % project_full_name
    # It will jump to https://github.com/author/repo/compare/version...author:repo
    url = requests.get(url).url
    url += '.patch'
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        content = r.text
    else:
        raise Exception("error on get diff for %s!" % project_full_name)
    
    diff_list = content.split('diff --git')

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
            added_code = []
            for part in parts:
                lines_of_code = filter(lambda x: (x) and (x[0] == '+'), part.splitlines())
                lines_of_code = [start_with_plus_regex.sub('', x) for x in lines_of_code]
                added_code.extend(lines_of_code)

            save_path = current_app.config['LOCAL_DATA_PATH']
            # save_path = '/Users/fancycoder/infox_data/result'
            file_path = '%s/added_code/%s/%s' % (save_path, project_full_name, file_full_name)
            file_dir = os.path.dirname(file_path)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            with open(file_path, 'w') as f:
                f.write("\n".join(added_code))
            
            try:
                if platform.system() == 'Darwin':
                    srcML_name = 'srcML'
                    srcml_ns = 'http://www.srcML.org/srcML/src'
                elif platform.system() == 'Linux':
                    srcML_name = 'src2srcml'
                    srcml_ns = 'http://www.sdml.info/srcML/src'
                
                srcML_result = os.popen('%s %s' % (srcML_name, file_path), 'r').read()
                
                name_list = filter(lambda x: (x) and (len(x) > 2), [x.text for x in ET.fromstring(srcML_result).iter(tag='{%s}name' % srcml_ns)])
                name_list = filter(lambda x: x not in language_tool.get_language_stop_words(language_tool.get_language(file_full_name)), name_list)
                func_list = []
                for x in ET.fromstring(srcML_result).iter(tag='{%s}function_decl' % srcml_ns):
                    func_name = x.find('{%s}name' % srcml_ns)
                    if func_name is not None:
                        if func_name.text is not None:
                            func_list.append(func_name.text)
                all_name_list.extend(name_list)
                all_func_list.extend(func_list)
            except:
                pass
    """
            
    return {'name_list': all_name_list, 'func_list': all_func_list}

if __name__ == '__main__':
    get_fork_changed_code_name_list('arturoc/ofxVideoRecorder')


