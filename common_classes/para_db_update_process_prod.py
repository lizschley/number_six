''' This is Step Three of the database update process, but for production or running like production in
    development.  Step 1 retrieves & Step 2 edits the data.  If it is truly production, Step 2 will be
    skipped. '''

import sys
from common_classes.para_db_update_process import ParaDbUpdateProcess
import helpers.no_import_common_class.utilities as utils


class ParaDbUpdateProcessProd(ParaDbUpdateProcess):
    '''
        ParaDbUpdateProcessProd will be run for updates that either use the run_as_prod method or that
        run in the actual production environment.  The process will do different things, based on which
        of the above scenarios is true. The main difference is that in development, you can send in
        blank guids and slugs, but in production, you never can, because development is the source of
        truth.
    '''

    def process_input_data_update_db(self):
        '''
        process_input_data_update_db is the main driver of the update process.  You can see the order
        that we process the data by the method names.
        '''
        self.validate_input_keys()
        self.build_preliminary_data()
        self.update_record_loop()
        self.add_or_delete_associations()

    def validate_input_keys(self):
        '''
        validate_input_keys ensures that the user is doing careful work

        It runs some tests on the input keys and errors with a message, if the tests fail
        '''
        if self.explicit_creates_in_prod():
            data = self.file_data
            sys.exit(f'Input error: explicit creates prohibited in prod or when run_as_prod: {data}')

        if self.incorrect_environment():
            data = self.input_data
            sys.exit(f'Input error: wrong process unless production or running as prod: {data}')

    def incorrect_environment(self):
        if self.input_data['is_prod'] or self.input_data['run_as_prod']:
            return False
        return True

    def explicit_creates_in_prod(self):
        '''
        explicit_creates_in_prod validates ensures that we do not have any add_ keys when we are running
        production or when we are mimicing the production process.  All production creates will be as if
        the data was first created in development and will now be created in production with the same
        unique keys (other than the id, which may or may not be the same)

        :return: returns True when it's a production run and there are input keys like add_*
        :rtype: bool
        '''
        if not self.input_data['is_prod'] and not self.input_data['run_as_prod']:
            return False
        return utils.dictionary_key_begins_with_substring(self.file_data, 'add_')

    def build_preliminary_data(self):
        '''
        build_preliminary_data will loop through input data and do the following:
        1. For blank slug or guids:
           if development, create unique key (guid or slug) and add record to create record.  Will NOT
           go into create record loop.  It will have a different create record loop

           if production, error out (new validation)

        2. Any associations should have a dev_id to unique key relationship in the input data.  These
           can be new and separate from the parent records. For example, if we forgot a reference or
           are adding a paragraph to a new group.  Or it could be  should have a dev_id to unique key
           for each foreign key.

        3. Delete associations will have the unique keys as part of the input data
        '''
