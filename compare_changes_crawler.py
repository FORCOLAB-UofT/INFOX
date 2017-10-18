import os
from selenium import webdriver
import requests

language_file_suffix = ['.h', '.c', '.cc', '.cpp', '.java']
stop_words = [',', '(', ')', ';', '.']

# Example:
#   compare('NeilBetham/Smoothieware')
#   It will return 26.
def compare(project_full_name):
    #It will jump to https://github.com/author/repo/compare/version...author:repo
    url = 'https://github.com/%s/compare' % project_full_name
    driver = webdriver.PhantomJS()
    try:
        driver.get(url)
        diff_list = driver.find_element_by_id("diff").find_element_by_id("files")
    except:
        print("error on get diff for %s!" % project_full_name)
        return -1

    changed_file_list = []
    total_changed_line_of_source_code = 0

    diff_num = 0
    while(True):
        try:
            diff = diff_list.find_element_by_id('diff-' + str(diff_num))
        except:
            # print("finish crawler on all diffs")
            break
        diff_num += 1

        # TODO(Luyao Ren)If the changed is too large, the result from github will
		# not show diff code first.Need more work to get diff files name/codes.
		try:
            diff_info = diff.find_element_by_class_name('file-info')
            changed_line, file = diff_info.text.split(' ')
            changed_file_list.append(file)
        except:
            break

        file_name, file_suffix = os.path.splitext(file)
        if file_suffix in language_file_suffix:
            total_changed_line_of_source_code += int(changed_line)
            changed_code = diff.text

            # This is for the case that "Large diffs are not rendered by default" on Github
            # Example:
            #     https://github.com/MarlinFirmware/Marlin/compare/1.1.x...SkyNet3D:SkyNet3D-Devel
            try:
                load_container = diff.find_element_by_class_name('js-diff-load-container')
                print("This file: %s need load code." % file)
                load_url = load_container.find_element_by_xpath('//include-fragment[1]').get_attribute('data-fragment-url')
                try:
                    changed_code = requests.get('https://github.com/' + load_url).text
                except:
                    print "Error on get load code!"
            except:
                pass

            word_lists = changed_code.split(' ')
            word_lists = filter(lambda x: (len(x) >= 2) and (x not in stop_words), word_lists)

    # print("changed file list:", changed_file_list)
    # print("total changed line (after filter) = %d" % total_changed_line_of_source_code)
    return total_changed_line_of_source_code

