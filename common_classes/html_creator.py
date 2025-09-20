import os
import settings
import pprint
from constants import html_page_data as page_data
from utilities import file_utils as utils


class HtmlCreator:
    ''' use to create html files of a type used frequently '''

    def __init__(self):
        ''' set up framework '''
        self.input_data = {}
        self.infile = ''
        self.outfile = ''

    def create_html_process(self):
        self.assign_data()
        self.create_html_file()

    def assign_data(self):
        self.input_data = self.build_input_data()
        pprint.pprint(self.input_data)
        outfile = self.input_data['files']['output_file']
        self.outfile = outfile if '/Users/eaffie/' in outfile else os.path.join(settings.BASE_DIR, outfile)
        self.infile = os.path.join(settings.BASE_DIR, self.input_data['files']['input_file'])
        print(f'Output file is {self.outfile}')

    def build_input_data(self):
        input_data = {}
        input_data['files'] = page_data.FILES
        input_data['add_to_imports'] = self.additional_imports()
        input_data['end_top_html'] = page_data.END_TOP_HTML
        input_data['add_to_framework'] = self.additional_framework()
        input_data['end_html'] = page_data.END_HTML
        return input_data

    def additional_imports(self):
        add_imports = []
        if page_data.FLAGS['modal']:
            add_imports = page_data.NEEDED_FOR_MODALS
        if page_data.FLAGS['table']:
            add_imports = add_imports + page_data.NEEDED_FOR_TABLE
        return add_imports

    def additional_framework(self):
        if page_data.FLAGS['accordian']:
            return page_data.ACCORDIAN_HTML
        return ''

    def create_html_file(self):
        utils.copy_file_from_source_to_target(self.infile, self.outfile)
        utils.append_file_from_array(self.input_data['add_to_imports'], self.outfile, 'a+')
        utils.write_file_from_string(self.input_data['end_top_html'], self.outfile, 'a+')
        utils.write_file_from_string(self.input_data['add_to_framework'], self.outfile, 'a+')
        utils.write_file_from_string(self.input_data['end_html'], self.outfile, 'a+')

    def append_additional_imports(self):
        utils.append_file_from_array(self.input_data['add_to_imports'], self.outfile, 'a+')
