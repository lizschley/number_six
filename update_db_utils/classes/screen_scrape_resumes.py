''' This is a class that will be reused and updated constantly.  Eventually may make a base
    class from it.  But right now I just want it to save me manual labor
'''
import requests
from bs4 import BeautifulSoup
from update_db_utils.classes.paragraph_db_input_creator import ParagraphDbInputCreator
import constants.resume as constants
import utilities.random_methods as utils


class ScreenScrapeResumes(ParagraphDbInputCreator):
    '''
        Loading data through Screenscraping will be different every time, but it should always implement
        ParagraphDbInputCreator
    '''

    def __init__(self, **kwargs):
        group_title = kwargs.get('group_title', 'Temporary')
        json_only = kwargs.get('json_only', False)
        updating = kwargs.get('updating', False)
        super().__init__(group_title, json_only, updating)
        if utils.key_in_dictionary(kwargs, 'url'):
            self.url = kwargs['url']
            self.html_path = None
        else:
            self.url = None
            self.html_path = kwargs['html_path']
        self.process_data['paragraphs'] = []
        self.process_data['before_work_experience'] = True
        self.process_data['before_education'] = True
        self.process_data['curr_company'] = ''
        self.process_data['counts'] = {'total': 0, 'cc': 0, 'ts': 0, 'mas': 0, 'ln': 0}

    def screen_scrape_html(self):
        ''' driver function for resume screen scraping '''
        html = self.retrieve_data()
        self.step_through_html(html)
        print(self.process_data['counts'])
        self.create_content([], self.process_data['paragraphs'])

    def retrieve_data(self):
        '''
        retrieve_data gets data from the url that is passed in
        '''
        if self.url:
            res = requests.get(self.url)
            html = res.text
        else:
            html = open(self.html_path).read()
        return html

    def step_through_html(self, html):
        ''' loop through spans '''
        soup = BeautifulSoup(html, features='lxml')
        spans = soup.find_all('span')
        for span in spans:
            span_text = span.get_text().strip()
            if not self.process_data['before_education']:
                return
            if len(span_text) < 4:
                continue
            if self.process_data['before_work_experience']:
                if constants.LOOKING_FOR['work_experience'] in span_text:
                    self.process_data['before_work_experience'] = False
                continue
            self.create_paragraph_data(span_text)

    def create_paragraph_data(self, span):
        ''' Loop through work experience to pull paragraphs '''
        if constants.LOOKING_FOR['education'] in span:
            self.process_data['before_education'] = False
            return
        for substr in constants.COMPANY_SUBSTR:
            if substr in span:
                self.process_data['curr_company'] = constants.COMPANIES[substr]
                return
        if len(span) > 10:
            self.create_para(span)

    def new_para(self):
        ''' These are the pargraph variables that do not have defaults in ParagraphDbInputCreator '''
        return {
            'subtitle': '',
            'note': '',
            'text': '',
            'short_title': ''
        }

    def create_para(self, span):
        ''' taking span text and using it to create a paragraph '''
        new_para = self.new_para()
        new_para['text'] = constants.TEXT['beg_para'] + span
        new_para['text'] += constants.TEXT['beg_tech_list'] + constants.TECH_LIST
        new_para['text'] += constants.TEXT['beg_company'] + self.process_data['curr_company']
        new_para['text'] += constants.TEXT['end_para']
        for substr in constants.COMPANY_SUBSTR:
            self.increment_counts(substr)
        self.process_data['paragraphs'].append(new_para)

    def increment_counts(self, substr):
        '''
           for these substring ('Medical', 'LexisNexis', 'Teachstone', 'Construct')
           increment the correct number of records
        '''
        self.process_data['counts']['total'] += 1
        if substr == 'Medical' and substr in self.process_data['curr_company']:
            self.process_data['counts']['mas'] += 1
            return
        if substr == 'LexisNexis' and substr in self.process_data['curr_company']:
            self.process_data['counts']['ln'] += 1
            return
        if substr == 'Teachstone' and substr in self.process_data['curr_company']:
            self.process_data['counts']['ts'] += 1
            return
        if substr == 'Construct' and substr in self.process_data['curr_company']:
            self.process_data['counts']['cc'] += 1
            return
