''' This is Step Three of the database update process.  Step 1 retrieves & Step 2 edits the data '''
import os
from common_classes.para_db_methods import ParaDbMethods
from portfolio.settings import BASE_DIR


OUT_JSON_PATH = os.path.join(BASE_DIR, 'data')


class ParaDbUpdateProcess(ParaDbMethods):
    '''
        ParaDbUpdateProcess updates (or if production or run_as_prod, creates) data based on
        self.input_data
    '''

    def __init__(self, input_data, updating=False):
        '''
        __init__ Assign the framework needed to ...
        '''
        super(ParaDbUpdateProcess, self).__init__(updating)
        self.input_data = input_data

    def process_input_data_update_db(self):
        print(f'self.input_data=={self.input_data}')
        print(f'self.updating=={self.updating}')
