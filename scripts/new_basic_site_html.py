''' Before creating the automated html file, alter the variables in constants/html_page_data.py
   Currently the important ones are FLAGS, FILES and END_HTML_VARIABLES
'''

# This is the script to create a new site
from common_classes.html_creator import HtmlCreator

if __name__ == '__main__':
    html_creator = HtmlCreator()
    html_creator.create_html_process()
    html_creator.create_carousel_html()
    print(html_creator.carousel_html)
