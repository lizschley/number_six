'''
    Reads a json file and either displays how it looks after basic paragraph processing
    or creates new paragraphs

:returns: nothing
'''
# pylint: disable=c0301
# from pprint import pprint
from update_db_utils.classes.screen_scrape_plant_db import ScreenScrapePlantDb


def run():
    '''
        Update this to make the kwargs and class to instantiate is correct
        >>> python manage.py runscript -v3  screen_scraper
    '''
    params = params_to_use()
    scraper = ScreenScrapePlantDb(**params)
    scraper.screen_scrape_html()


def params_to_use():
    '''
        These are the kwargs to send into the screen scraping class you are instantiating

        Note - to use the request object to read a web page, return also {'url': url_value}
               as part of the dictionary
    '''
    return {
        'json_only': True,
        'updating': False
    }
