''' uses base class for csv processing '''
# pylint: disable-msg=C0103
from common_classes.csv_processor import CsvProcessor


class CommunityCode(CsvProcessor):
    ''' will create repetitive html and js using spreadsheet data '''
    FILE_PATH = 'file_upload/urban_habitat.csv'

    def __init__(self, input_path=FILE_PATH):
        super().__init__(input_path)
        self.show_results()

    def show_results(self):
        print(self.intial_dict)















