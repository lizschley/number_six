'''
    Reads a json file and either displays how it looks after basic paragraph processing
    or creates new paragraphs

:returns: nothing
'''
# pylint: disable=c0301
import os
# from pprint import pprint
from update_db_utils.classes.screen_scrape_resumes import ScreenScrapeResumes
import constants.scripts as constants


def run():
    '''
        Update this to make the kwargs and class to instantiate is correct
        >>> python manage.py runscript -v3  screen_scraper
    '''
    params = params_to_use()
    file_list = list_of_files(constants.INPUT_FOR_HTML)
    for filepath in file_list:
        params['html_path'] = filepath
        scraper = ScreenScrapeResumes(**params)
        scraper.screen_scrape_html()


def list_of_files(in_directory):
    '''
    list_of_files gets a list of files from the input directory

    :param in_directory: path to a directory containing files to put in a list
    :type in_directory: str
    :return: list of filepaths
    :rtype: list
    '''
    file_list = []
    for filename in os.listdir(in_directory):
        temp = filename.split('.')
        if len(temp) < 2 or temp[1] != 'html':
            continue
        file_path = os.path.join(in_directory, filename)
        if os.path.isfile(file_path):
            file_list.append(file_path)
    return file_list


def params_to_use():
    '''
        These are the kwargs to send into the screen scraping class you are instantiating

        Note - to use the request object to read a web page, return also {'url': url_value}
               as part of the dictionary
    '''
    return {
        'group_title': 'Temporary',
        'json_only': True,
        'updating': False
    }
