''' This is a class that will be reused and updated constantly.  Eventually may make a base
    class from it.  But right now I just want it to save me manual labor
'''
import requests
from bs4 import BeautifulSoup
from update_db_utils.classes.paragraph_db_input_creator import ParagraphDbInputCreator
import utilities.random_methods as utils


class ScreenScrapeResumes(ParagraphDbInputCreator):
    '''
        Loading data through Screenscraping will be different every time, but it should always implement
        ParagraphDbInputCreator
    '''

    COMPANY_SUBSTR = ('Medical', 'LexisNexis', 'Teachstone', 'Construct')
    LOOKING_FOR = ('Work Experience')

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

    def process_data(self):
        ''' driver function for resume screen scraping '''
        html = self.retrieve_data()
        self.step_through_html(html)

    def retrieve_data(self):
        '''
        retrieve_data gets data from the url that is passed in
        '''
        if self.url:
            html = requests.get(self.url)
        else:
            html = open(self.html_path).read()
        return html

    def step_through_html(self, html):
        ''' loop through spans '''
        soup = BeautifulSoup(html, features='lxml')
        spans = soup.find_all('span')

        technologies = {'before_work_experience': True}
        technologies['tech_list'] = []
        para_data = {'before_education': True}
        para_data['curr_company'] = ''
        para_data['curr_dates'] = ''
        para_data['paragraphs'] = []
        para_data['beg_para'] = ''
        for span in spans:
            if technologies['before_work_experience']:
                technologies = self.process_technologies(span, technologies)
            elif para_data['before_education']:
                para_data = self.create_paragraph_data(self, span, para_data)
            else:
                continue

    def process_technologies(self, span, technologies):
        ''' get list of technologies, can narrow it down manually '''
        span_text = span.get_text()
        if 'Work Experience' in span_text:
            technologies['before_work_experience'] = False
            return technologies
        breakpoint()
        return technologies

    def create_paragraph_data(self, span, para_data, technologies):
        ''' Loop through work experience to pull paragraphs '''
        span_text = span.get_text()
        if 'Education' in span_text:
            para_data['before_education'] = False
            return para_data
        breakpoint()
        return para_data
