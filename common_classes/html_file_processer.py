'''class for any boto3 automation '''
# pylint: disable-msg=C0103
import sys
from bs4 import BeautifulSoup
import constants.html_lookup as lookup
import helpers.no_import_common_class.utilities as utils


class HtmlFileProcesser:
    ''' Use for updating template/base_file.html '''
    def __init__(self, lookup_key, process='base_html'):
        if process == 'base_html':
            self.data = lookup.BASE_FILE_DATA[lookup_key]
        self.data['base_html_path'] = lookup.BASE_FILE_DATA['base_html_path']
        self.lookup_key = lookup_key
        self.curr_version = ''

    def update_base_html_s3_versions(self, new_version):
        ''' driver to update base.html '''
        prior_version = self.replace_path_attribute()
        print(f'lookup_key == {self.lookup_key}')
        self.curr_version = new_version
        # prior version will be used for deleting s3 version
        return prior_version

    def replace_path_attribute(self):
        ''' learning '''
        attr = self.data['attribute']
        html = open(self.data['base_html_path']).read()
        soup = BeautifulSoup(html, features='lxml')
        el = soup.find(id=self.data['id'])
        print(f'element found is {el}')
        path_info = self.parse_path(el[attr])
        # add check for error in parse path
        print(f'path == {path_info["new_path"]}')
        # el[self.data['attribute']] = new_path
        # -----------> example
        # https://stackoverflow.com/questions/60201175/set-xml-attribute-value-with-beautifulsoup4
        # soup = bs(svg, 'html.parser')
        # circle = soup.find('circle')
        # circle['fill'] = 'blue'
        # soup.find('circle').replace_with(circle)

        return path_info['prior_version']

    def parse_path(self, path):
        '''
        parse_path takes path and returns a dictionary with the path with the updated version
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
        # path_list[0] should be beginning of path
        # path_list[1] should be the prior version
        # path_list[2] should be hte end of the path
        # new path should be path_list[0] + '_' + new_version + '.' + path_list[2]
        print(f'original path == {path}')
        print(f'path_list == {path_list}')
        path_info['prior_version'] = 'prior version from parse_path'
        path_info['new_path'] = 'new path from parse_path'
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

    @staticmethod
    def wrong_list_length(temp_list):
        ''' if the list length is wrong, need to error out and fix code '''
        if len(temp_list) != 2:
            return True
        return False
