import os
import sys
import settings
from constants import html_page_data as page_data
from utilities import file_utils as utils
from utilities import random_methods as helper


class HtmlCreator:
    ''' use to create html files of a type used frequently '''

    def __init__(self):
        ''' set up framework '''
        self.input_data = {}
        self.infile = ''
        self.outfile = ''
        self.datafile = ''

    def create_html_process(self):
        self.assign_data()
        self.create_html_file()

    def assign_data(self):
        base_dir = settings.BASE_DIR
        self.input_data = self.build_input_data()
        outfile = self.input_data['files']['output_file']
        datafile = self.input_data['files']['data_file']
        self.outfile = outfile if '/Users/eaffie/' in outfile else os.path.join(base_dir, outfile)
        self.datafile = datafile if '/Users/eaffie/' in datafile else os.path.join(base_dir, datafile)
        self.infile = os.path.join(base_dir, self.input_data['files']['input_file'])
        # print(f'Output file is {self.outfile}')

    def create_html_file(self):
        utils.copy_file_from_source_to_target(self.infile, self.outfile)
        utils.append_file_from_array(self.input_data['add_to_imports'], self.outfile, 'a+')
        utils.write_file_from_string(self.input_data['end_top_html'], self.outfile, 'a+')
        utils.write_file_from_string(self.input_data['top_end_html'], self.outfile, 'a+')
        self.process_additional_framework()
        utils.write_file_from_string(self.input_data['end_html'], self.outfile, 'a+')

    def build_input_data(self):
        input_data = {}
        input_data['files'] = page_data.FILES
        input_data['add_to_imports'] = self.additional_imports()
        input_data['end_top_html'] = page_data.END_TOP_HTML
        input_data['top_end_html'] = page_data.TOP_END_HTML
        input_data['end_html'] = page_data.END_HTML
        return input_data

    def additional_imports(self):
        add_imports = []
        if page_data.FLAGS['accordion']:
            add_imports = add_imports + page_data.NEEDED_FOR_ACCORDION
        if page_data.FLAGS['modal']:
            add_imports = add_imports + page_data.NEEDED_FOR_MODALS
        if page_data.FLAGS['table']:
            add_imports = add_imports + page_data.NEEDED_FOR_TABLE
        return add_imports

    def process_additional_framework(self):
        if page_data.FLAGS['accordion']:
            self.accordion_html = self.accordion_html()
            utils.write_file_from_string(self.accordion_html['html_top'], self.outfile, 'a+')
            self.accordion_html['variables']['rep_var']['index'] += 1
            self.process_accordion_repeatable_data()

    def accordion_html(self):
        return {
            'variables': page_data.ACCORDION_HTML_VARIABLES,
            'html_top': page_data.ACCORDION_HTML_TOP,
            'end_repeatable': page_data.ACCORDIAN_END_REPEATABLE,
            'end_accordion': page_data.ACCORDION_BOTTOM_HTML
        }

    def process_accordion_repeatable_data(self):
        # Open input file in read mode
        with open(self.datafile, 'r') as file:
            # Read all lines into a list
            self.lines = file.readlines()
            self.create_and_write_accordion_items()

    def create_and_write_accordion_items(self):
        for line in self.lines:
            if not helper.valid_non_blank_string(line):
                continue
            self.process_line(line)

    # Note - we need the button text before ready_for_item (<p> lines) can be true within an accordion
    # We must have at least one item line before another button
    # This is coded for expected data, if data is different need different code.
    # See dr_brenner_gleanings in one of following directories: basic_site_html or scratch
    def process_line(self, line):
        if helper.is_header(line) & self.accordion_html['variables']['rep_var']['end_prior_repeatable']:
            self.end_accordion_item()
            utils.write_file_from_string(line, self.outfile, 'a+')
            return
        if helper.is_header(line):
            utils.write_file_from_string(line, self.outfile, 'a+')
            return
        if helper.is_button(line):
            if self.accordion_html['variables']['rep_var']['end_prior_repeatable']:
                self.end_accordion_item()
            self.accordion_html['variables']['rep_var']['button_text'] = self.strip_button_tags(line)
            utils.write_file_from_string(page_data.ACCORDION_REPEATABLE_HTML, self.outfile, 'a+')
            self.accordion_html['variables']['rep_var']['ready_for_item_lines'] = True
            return
        if not self.accordion_html['variables']['rep_var']['ready_for_item_lines']:
            print('no lines without a button.')
            print(f'variables" {self.accordion_html['variables']['rep_var']}')
            print(f'line is: {line}')
            sys.exit()
        line = line if '<p>' in line else '<p>' + line
        utils.write_file_from_string(line, self.outfile, 'a+')
        self.accordion_html['variables']['rep_var']['end_prior_repeatable'] = True

    def end_accordion_item(self):
        utils.write_file_from_string(self.accordion_html['end_repeatable'], self.outfile, 'a+')
        self.accordion_html['variables']['rep_var']['end_prior_repeatable'] = False
        self.accordion_html['variables']['rep_var']['ready_for_item_lines'] = False

    # this is for known data, with no end_button tags. Flexible code....
    def strip_button_tags(self, line):
        if '<button>' in line:
            temp = line.split('<button>')
        return temp[1].strip()
