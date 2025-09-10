# This is the script to create a new site
from basic_site_html import page_data
from common_classes.html_creator import HtmlCreator

MODAL = False
TABLE = False

if __name__ == '__main__':
    html_creator = HtmlCreator(page_data.create_input_data())
    html_creator.create_html_file()
    # file should be written in html_creator.outfile.


def create_input_data():
    input_data = page_data.FILES
    input_data['end_html'] = page_data.end_html()
    input_data['extra_head_imports'] = page_data.head_imports()
    return input_data
