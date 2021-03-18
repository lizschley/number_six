''' This is a class that will be reused and updated constantly.  Eventually may make a base
    class from it.  But right now I just want it to save me manual labor
'''
import copy
import pprint
import sys
import requests
from bs4 import BeautifulSoup
from update_db_utils.classes.paragraph_db_input_creator import ParagraphDbInputCreator
import constants.plants as constants
import utilities.random_methods as utils


class ScreenScrapePlantDb(ParagraphDbInputCreator):
    '''
        Loading data through Screenscraping will be different every time, but it should always implement
        ParagraphDbInputCreator
    '''

    def __init__(self, **kwargs):
        group_title = 'Native Plant Descriptions'
        json_only = kwargs.get('json_only', True)
        updating = kwargs.get('updating', False)
        super().__init__(group_title, json_only, updating)
        self.url = constants.AC_NATIVE_PLANT_URL
        self.subtitle_note = constants.AC_NATIVE_SUBTITLE_NOTE
        self.process_data['references'] = []
        self.process_data['paragraphs'] = []
        self.process_data['num_records'] = 0

    def screen_scrape_html(self):
        ''' driver function for resume screen scraping '''
        html = self.retrieve_data()
        self.step_through_html(html)
        print(f'processed {self.process_data["num_records"]} records')
        # self.create_content(self.process_data['references'], self.process_data['paragraphs'])

    def retrieve_data(self):
        '''
            retrieve_data gets data from the url that is passed in
        '''
        html = None
        if self.url:
            res = requests.get(self.url)
            html = res.text

        return html

    def step_through_html(self, html):
        ''' loop through spans '''
        soup = BeautifulSoup(html, features='lxml')
        rows = soup.find_all('tr')
        for idx, row in enumerate(rows):
            cells = row.findAll('td')
            if len(cells) != 5:
                continue
            if idx > 3:
                self.process_row(cells)
                self.create_para()
                continue
            self.test_headers(cells)

    def test_headers(self, cells):
        ''' ensure headers are correct '''
        for idx, cell in enumerate(cells):
            if constants.AC_NATIVE_PLANT_HEADERS[idx] in cell.get_text():
                print(f'working ok: text == {cell.get_text()}')
            else:
                print((f'error! idx=={idx} template=={constants.AC_NATIVE_PLANT_HEADERS[idx]}; '
                       f'text == {cell.get_text()}'))

    def process_row(self, cells):
        ''' loop through table columns for the given row. Process each one '''
        self.process_data['new_para'] = copy.deepcopy(self.new_para_dictionary())
        self.process_data['text_dictionary'] = copy.deepcopy(constants.TEXT_TEMPLATE)
        for idx, cell in enumerate(cells):
            col = constants.AC_NATIVE_PLANT_HEADERS[idx]
            print(f'idx=={idx} col=={col} size cells = {len(cells)}')
            self.process_data[col] = {}
            if col == 'Scientific/Common Name':
                self.name_column(cell, col)
            elif col == 'Stormwater Facilities':
                self.process_data['text_dictionary'][col] = self.extract_text_into_list(cell)
            elif col == 'Recommended Uses':
                self.uses_column(cell, col)
            elif col == 'Plant Needs':
                text_list = self.extract_text_into_list(cell)
                self.process_data['text_dictionary']['Growing Conditions'] = text_list
            elif col == 'Plant Characteristics':
                self.characteristics_column(cell, col)
            else:
                continue

    def name_column(self, cell, key):
        ''' should have a reference, subtitle, native_status '''
        cell = self.extract_links(cell, key)
        text_list = self.extract_text_into_list(cell)
        for idx, text in enumerate(text_list):
            text = text.strip()
            if idx == 0:
                subtitle = self.process_data[key]['scientific_name'] + '; ' + text
                self.process_data['new_para']['subtitle'] = subtitle
                if len(text) > 2:
                    self.process_data['new_para']['short_title'] = text
            elif idx == 1:
                if len(text) > 2:
                    self.process_data['text_dictionary']['Type of Plant'].append(text)
            elif idx == 2:
                if 'Native' in text:
                    new_text = text.replace('Native', '').strip()
                    if len(new_text) > 2:
                        self.process_data['text_dictionary']['Native Status'].append(new_text)
            else:
                continue

    @staticmethod
    def extract_text_into_list(cell):
        ''' extract_text_into_list - takes the remaining contents an strips whitespace and tags '''
        text_list = []
        for text in cell.contents:
            if text.string is None:
                continue
            new_text = text.string.strip()
            if len(new_text) > 0:
                text_list.append(new_text)
        return text_list

    def extract_links(self, cell, key):
        ''' Extract the information from the usda link in the first column'''
        for a in cell('a'):
            if cell.a is None:
                continue
            link = cell.a.extract()
            short_text = link.get_text()
            check_url = link['href']
            if 'usda.gov' not in check_url:
                continue
            self.assign_new_ref(key, check_url, short_text)
        return cell

    def assign_new_ref(self, key, usda_url, short_text):
        ''' use url and knowledge of data to create new a new reference record '''
        url = self.return_usda_url(usda_url)
        self.process_data[key]['scientific_name'] = short_text.replace(' ', '-')
        link_text = 'USDA_' + short_text.title().replace(' ', '')
        short_text = 'USDA ' + short_text if len(short_text) < 25 else short_text
        self.process_data['new_ref'] = self.new_ref_dictionary(link_text, url, short_text)
        self.process_data['new_para']['link_text_list'].append(link_text)

    def return_usda_url(self, usda_url):
        '''
            build_usda_url returns a https url that does not have java in the path

            :param check_url: [description]
            :type check_url: [type]
        '''
        temp_list = usda_url.split('=')
        if len(temp_list) != 2:
            sys.exit(f'weird issue with the usda url: {usda_url}')
            return None
        return constants.USDA_BASE_PLANT_URL + temp_list[1].strip()

    def uses_column(self, cell, key):
        ''' assign this to wildlife for now.  Will have to change some text '''
        uses_list = self.extract_text_into_list(cell)
        two_lists = utils.separate_lists(uses_list, constants.USES_LIST)
        self.process_data['text_dictionary']['Wildlife Value'] = two_lists['fix_list']
        self.process_data['text_dictionary']['Uses'] = two_lists['new_list']

    def characteristics_column(self, cell, col):
        ''' plant characteristics, will parse '''
        lookup = constants.LOOKUP[col]
        text_list = self.extract_text_into_list(cell)
        where = {'key': '', 'save_text': ''}
        for text in text_list:
            if len(where['save_text']) > 3:
                self.process_data['text_dictionary'][where['key']] = where['save_text'] + ' ' + text
                where['save_text'] = ''
                where['key'] = ''
                continue
            where = self.characteristic_lookup(lookup, text)
            if len(where['save_text']) > 3:
                continue
            self.process_data['text_dictionary'][where['key']].append(text)

    @staticmethod
    def characteristic_lookup(lookup, text):
        ''' Add text to appropriate text dictionary key '''
        key = 'Characteristics'
        save_text = ''
        for string in lookup:
            if string in text:
                if string == 'Est':
                    key = 'Size'
                if string == 'Foliage':
                    key = 'Leaves'
                    save_text = text if text[-1] == ':' else ''
                elif string in ('Flower', 'Bloom'):
                    key = 'Flowers'
                    save_text = text if text[-1] == ':' else ''
        return {'key': key, 'save_text': save_text}

    @staticmethod
    def new_para_dictionary():
        ''' Need defaults and link_text_list '''
        return {
            'subtitle': '',
            'note': constants.AC_NATIVE_SUBTITLE_NOTE,
            'text': '',
            'short_title': '',
            'link_text_list': ['AlbemarleCounty_NativePlantList_on20210317']
        }

    @staticmethod
    def new_ref_dictionary(link_text, url, short_text):
        ''' Need all data '''
        return {
            'link_text': link_text,
            'url': url,
            'short_text': short_text
        }

    def create_para(self):
        ''' taking span text and using it to create a paragraph '''
        self.increment_counts()
        self.process_data['new_para']['text'] = self.create_text()
        self.process_data['paragraphs'].append(self.process_data['new_para'])
        self.process_data['references'].append(self.process_data['new_ref'])

    def create_text(self):
        ''' remaining process '''
        self.refine_wildlife()
        printer = pprint.PrettyPrinter(indent=1, width=120)
        printer.pprint(self.process_data["text_dictionary"])
        breakpoint()
        return ''

    def refine_wildlife(self):
        ''' Move text to appropriate text dictionary key '''
        fix_list = self.process_data['text_dictionary']['Wildlife Value']
        res = utils.separate_lists(fix_list, constants.LOOKUP['Caterpillars'])
        self.process_data['text_dictionary']['Caterpillars'] = res['new_list']
        res = utils.separate_lists(res['fix_list'], constants.LOOKUP['Growing Conditions'])
        self.process_data['text_dictionary']['Wildlife Value'] = res['fix_list']
        self.process_data['text_dictionary']['Growing Conditions'] += res['new_list']


    def increment_counts(self):
        '''
            increment number of records
        '''
        self.process_data['num_records'] += 1
