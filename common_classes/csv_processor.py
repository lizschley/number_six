''' base class for csv processing '''
# pylint: disable-msg=C0103
import os
import settings
import utilities.random_methods as utils


class CsvProcessor:
    ''' Use for csv to dict, inherit to not reinvent the wheel '''

    def __init__(self, file_path, data_dir='data'):
        ''' worry about reusability after it's working '''
        # 'file_upload/urban_habitat.csv'
        self.intial_dict = utils.dictionary_list_from_csv(os.path.join(settings.BASE_DIR, file_path))
        self.base_output_path = os.path.join(settings.BASE_DIR, data_dir)
        self.curr_row = {}

    def process_rows(self):
        for row in self.intial_dict:
            self.process_row(row)

    # this will most likely be replaced by inheriting class
    def process_row(self, row):
        print('in base class')
        self.curr_row = row
        print(row)
