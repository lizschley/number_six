import os
import settings
from utilities import file_utils as utils


class HtmlCreator:
    ''' use to create html files of a type used frequently '''

    def __init__(self, input_data):
        ''' worry about reusability after it's working '''
        # 'file_upload/urban_habitat.csv'
        self.create_html_file()
        self.data = input_data
        self.outfile = os.path.join(settings.BASE_DIR, input_data['out_file'])
        self.infile = os.path.join(settings.BASE_DIR, input_data['in_file'])
        print(f'in file == {self.infile}')
        print(f'inout file == {self.outfile}')

    def create_html_file(self, infile, outfile):
        newfile = utils.copy_file_from_source_to_target(self.infile, self.outfile)

    def loop_through_and_append(self):
        # append after creting the initial file
        # end of random file might have everything I need
