import os
import sys
import settings
from constants import html_page_data as page_data
from data.tasks import html_utilities as text
from utilities import file_utils as utils
from utilities import random_methods as helper

LAST_LINE = '~~end~~'


class HtmlCreator:
    ''' use to create html files of a type used frequently '''

    def __init__(self):
        ''' set up framework '''
        self.input_data = {}
        self.infile = ''
        self.outfile = ''
        self.datafile = ''
        self.accordion_html = {}
        self.accordion_var = {}
        self.carousel_html = ''

    def create_html_process(self):
        self.assign_data()
        self.create_html_file()

    def assign_data(self):
        base_dir = settings.BASE_DIR
        self.input_data = self.build_input_data()
        outfile = self.input_data['files']['output_file']
        self.outfile = outfile if '/Users/eaffie/' in outfile else os.path.join(base_dir, outfile)
        self.infile = os.path.join(base_dir, self.input_data['files']['input_file'])
        if helper.key_in_dictionary(self.input_data['files'], 'data_file'):
            datafile = self.input_data['files']['data_file']
            self.datafile = datafile if '/Users/eaffie/' in datafile else os.path.join(base_dir, datafile)

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

    def create_carousel_html(self):
        self.carousel_html = page_data.TOP_CAROUSEL_HTML
        self.carousel_html += text.make_carousel_item_divs(page_data.CAROUSEL_DATA)
        self.carousel_html += page_data.BOTTOM_CAROUSEL_HTML

    def additional_imports(self):
        add_imports = []
        if page_data.FLAGS['accordion']:
            add_imports = add_imports + page_data.NEEDED_FOR_ACCORDION
        if page_data.FLAGS['modal']:
            add_imports = add_imports + page_data.NEEDED_FOR_MODAL
        if page_data.FLAGS['table']:
            add_imports = add_imports + page_data.NEEDED_FOR_TABLE
        if page_data.FLAGS['carousel']:
            add_imports = add_imports + page_data.NEEDED_FOR_CAROUSEL
        if page_data.FLAGS['modal']:
            add_imports = add_imports + page_data.NEEDED_FOR_MODAL
        return add_imports

    def process_additional_framework(self):
        if page_data.FLAGS['accordion']:
            self.accordion_html = self.assign_accordion_html()
            utils.write_file_from_string(self.accordion_html['top'], self.outfile, 'a+')
            self.process_accordion_repeatable_data()
            utils.write_file_from_string(self.accordion_html['bottom'], self.outfile, 'a+')
        if page_data.FLAGS['modal']:
            utils.write_file_from_string(page_data.MODAL_HTML_ANCHOR, self.outfile, 'a+')

    def assign_accordion_html(self):
        self.accordion_var = page_data.ACCORDION_HTML_VARIABLES
        return {
            'top': page_data.ACCORDION_HTML_TOP,
            'bottom': page_data.ACCORDION_HTML_BOTTOM,
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
        input = self.accordion_var
        if self.test_for_output_item(line, input):
            self.accordion_var['index'] += 1
            kwargs = self.accordion_var
            utils.write_file_from_string(text.create_accordion_item(**kwargs), self.outfile, 'a+')
            self.accordion_var['body_lines'] = []
            self.accordion_var['button_text'] = ''
        if helper.is_header(line):
            utils.write_file_from_string(line, self.outfile, 'a+')
            self.accordion_var['wrote_header'] = True
            return
        if helper.is_button(line):
            self.accordion_var['button_text'] = self.strip_button_tags(line)
            return
        self.accordion_var['body_lines'].append(line)

    def test_for_output_item(self, line, input):
        if helper.valid_non_blank_string(input['button_text']) and len(input['body_lines']) > 0:
            if line == LAST_LINE or helper.is_button(line) or helper.is_header(line):
                return True
            return False

        if self.file_input_order_error(line, input):
            print(f'len_ body_lines: {len(input['body_lines'])}')
            print('button_text: ' + input['button_text'])
            print('line: ' + line)
            sys.exit('Need to output both button text and item text for this to work correctly')
        return False

    def file_input_order_error(self, line, input):
        if (input['index'] == input['orig_index']):
            return False
        if input['wrote_header']:
            self.accordion_var['wrote_header'] = False
            return False
        if line == LAST_LINE:
            return True
        if helper.is_button(line):
            return True
        if helper.is_header(line):
            return True
        return False

    # this is for known data, with no end_button tags. Flexible code....
    def strip_button_tags(self, line):
        if '<button>' in line:
            temp = line.split('<button>')
        return temp[1].strip()
