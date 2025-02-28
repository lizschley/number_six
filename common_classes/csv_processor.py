''' base class for csv processing '''
# pylint: disable-msg=C0103
import os
import settings
import utilities.random_methods as utils


class CsvProcessor:
    ''' Use for csv to dict, inherit to not reinvent the wheel '''

    def __init__(self, file_path):
        ''' worry about reusability after it's working '''
        # 'file_upload/urban_habitat.csv'
        self.intial_dict = utils.dictionary_list_from_csv(os.path.join(settings.BASE_DIR, file_path))
        self.curr_row = {}
        self.process_rows()

    def process_rows(self):
        print('in base process_rows')
