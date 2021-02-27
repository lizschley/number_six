'''class for any boto3 automation '''
# pylint: disable-msg=C0103
import shutil
from bs4 import BeautifulSoup
import constants.html_lookup as lookup
import utilities.random_methods as utils


class BaseHtmlProcesser:
    ''' Use for updating template/base_file.html '''
    def __init__(self, lookup_key, process='base_html'):
        if process == 'base_html':
            self.data = lookup.BASE_FILE_DATA[lookup_key]
        self.data['base_html_path'] = lookup.BASE_FILE_DATA['base_html_path']
        self.data['new_base_html'] = lookup.BASE_FILE_DATA['new_base_html']
        self.lookup_key = lookup_key
        self.curr_version = ''

    def update_base_html_s3_versions(self, new_version):
        ''' driver to update base.html '''
        self.curr_version = new_version
        path_info = self.replace_path_attribute()
        return path_info

    def replace_path_attribute(self):
        '''
        replace_path_attribute uses beautifulsoup to find an element by id

        :return: either the prior version (to be used in the future to delete file on S3) or error msg
        :rtype: dictionary
        '''
        attr = self.data['attribute']
        html = open(self.data['base_html_path']).read()
        soup = BeautifulSoup(html, features='lxml')
        el = soup.find(id=self.data['id'])
        path_info = self.new_path(el[attr])
        if utils.key_in_dictionary(path_info, 'error'):
            return path_info
        el[attr] = path_info['new_path']
        soup.find(id=self.data['id']).replace_with(el)
        str_element = str(el)
        params = self.params_for_replace_line_in_file(str_element)
        utils.replace_line(**params)
        shutil.move(self.data['new_base_html'], self.data['base_html_path'])
        return path_info

    def new_path(self, path):
        '''
        new_path takes path and returns a dictionary with the path with the updated version
        and also the prior version

        :param path: path from base.html for the file that we are currently parsing
        :type path: str
        :return: dictionary with the updateed path and also the prior version
        :rtype: dictionary
        '''
        path_info = {}
        result = self.split_path(path)
        if utils.key_in_dictionary(result, 'error'):
            return result
        path_list = result['path_list']
        path_info['prior_version'] = path_list[1]
        path_info['new_path'] = path_list[0] + '_' + self.curr_version + '.' + path_list[2]
        print(f'orig path == {path}')
        print(f'new path  == {path_info["new_path"]}')
        return path_info

    def split_path(self, in_str):
        '''
        split_path prepares the path for parsing, by splitting it into three pieces

        :param in_str: path (href for css file or src for javascript file)
        :type in_str: str
        :return: either an error or the path_list with the three pieces
        :rtype: dictionary
        '''
        path_data = {}
        path_data['path_list'] = []

        split_vars = ['_', '.']
        temp_str = in_str
        for split_var in split_vars:
            temp_list = temp_str.split(split_var)
            if self.wrong_list_length(temp_list):
                path_data['error'] = f'unexpected path ({in_str}) format.  Splitting on {split_var}'
                return path_data
            path_data['path_list'].append(temp_list[0])
            temp_str = temp_list[1]
        path_data['path_list'].append(temp_str)
        return path_data

    def params_for_replace_line_in_file(self, new_line):
        '''
        params_for_replace_line_in_file returns the input params to replace one line in a file

        :param new_line: line to be replaced, always indenting 4
        :type new_line: str
        :return: input to the replace_line function
        :rtype: dictionary that will become **kwargs
        '''
        indented_line = '    ' + new_line
        return {
            'in_file': self.data['base_html_path'],
            'out_file': self.data['new_base_html'],
            'sub_str': self.data['id'],
            'new_line': indented_line
        }

    @staticmethod
    def wrong_list_length(temp_list):
        ''' if the list length is wrong, need to error out and fix code '''
        if len(temp_list) != 2:
            return True
        return False
