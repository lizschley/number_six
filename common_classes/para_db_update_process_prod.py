''' This is Step Three of the database update process, but for production or running like production in
    development.  Step 1 retrieves & Step 2 edits the data.  If it is truly production, Step 2 will be
    skipped (unless someone is messing things up). '''

import sys
import uuid
import pprint
from django.utils.text import slugify
from common_classes.para_db_update_process import ParaDbUpdateProcess
import constants.crud as crud
import helpers.no_import_common_class.utilities as utils
import utilities.random_methods as methods


class ParaDbUpdateProcessProd(ParaDbUpdateProcess):
    '''
        ParaDbUpdateProcessProd will be run for updates that either use the run_as_prod method or that
        run in the actual production environment.  The process will do different things, based on which
        of the above scenarios is true. The main difference is that in development, you can send in
        blank guids and slugs, but in production, you never can, because development is the source of
        truth.
    '''

    def __init__(self, input_data, updating):
        '''
        __init__ stores the input data and provides the necessary framework to process the input data.
        This is mostly the same as the normal (not production or run_as_prod) data
        '''
        super(ParaDbUpdateProcessProd, self).__init__(input_data, updating)
        self.prod_results = {}
        self.only_delete = False
        if len(self.file_data.keys()) in range(1, 3):
            self.only_delete = True
            for key in self.file_data.keys():
                if key not in crud.DELETE_KEYS:
                    self.only_delete = False

        if self.only_delete:
            return

        try:
            self.record_lookups = self.file_data.pop('record_lookups')
        except KeyError:
            if self.input_data['is_prod']:
                sys.exit(crud.RECORD_LOOKUP_MESSAGE_PROD)
            else:
                sys.exit(crud.RECORD_LOOKUP_MESSAGE_DEV)

    def process_input_data_update_db(self):
        '''
        process_input_data_update_db is the main driver of the update process.  You can see the order
        that we process the data by the method names.
        '''
        # print(f'input_data == {self.input_data}')
        # print(f'file_data == {self.file_data}')
        print(f'only delete == {self.only_delete}')
        if self.only_delete:
            self.deleting_associations()
            sys.exit('Exiting after only deleting associations')

        self.validate_input_keys()
        self.preliminary_record_setup()
        if not self.updating:
            print('-------------------------------------------------------------')
            printer = pprint.PrettyPrinter(indent=1, width=120)
            printer.pprint(self.process_data)
            print('-------------------------------------------------------------')
            printer.pprint(self.record_lookups)
            return
        self.create_record_loop()
        self.update_record_loop()
        # We are only doing deletes here.  The adds are done in create_record_loop
        self.deleting_associations()

    def deleting_associations(self):
        '''
        deleting_associations is always called, but usually it is called at the very end of processing.
        The purpose of this method is to allow a user to delete associations in production without
        running Step One with a run_as_prod argument
        '''
        self.add_or_delete_associations()
        print('----------------------------------------------------------------')
        # Todo: move the delete process data to prod_results and then delete the process data print
        print('-------------------Process Data----------------------------------')
        printer = pprint.PrettyPrinter(indent=1, width=120)
        printer.pprint(self.process_data)
        print('------------------prod_results-----------------------------------')
        printer = pprint.PrettyPrinter(indent=1, width=120)
        self.add_delete_associations_to_prod_results()
        printer.pprint(self.prod_results)

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

        if self.not_run_as_prod_prep():
            if self.input_data['is_prod']:
                sys.exit(crud.RECORD_LOOKUP_MESSAGE_PROD + ' -- in validate input')
            else:
                sys.exit(crud.RECORD_LOOKUP_MESSAGE_DEV + ' -- in validate input')

    def not_run_as_prod_prep(self):
        '''
        not_run_as_prod_prep is an error in the input data lookup

        :return: True if there is an error, else False
        :rtype: bool
        '''
        for key in crud.UPDATE_RECORD_KEYS:
            if key in crud.ASSOCIATION_RECORD_KEYS:
                continue
            try:
                print(f'record lookup for {key} == {self.record_lookups[key]}')
            except KeyError:
                return True
        print('----------------------------------------------------------------')
        return False

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

    def preliminary_record_setup(self):
        '''
        preliminary_record_setup will loop through input data and set up the data in one of three
        different ways:
            1. Non-association records with no unique field
            2. Non-association records with a unique field
            3. Always adds association records to the create list, because until all the foreign records
               are created, we will not be able to do a find before creating an association
        '''
        for key in crud.UPDATE_RECORD_KEYS:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            self.prod_results[key] = {'created': [], 'updated': []}
            for record in self.file_data[key]:
                if key in crud.ASSOCIATION_RECORD_KEYS:
                    self.prod_results[key]['deleted'] = []
                    self.process_data[key]['create'].append(record)
                    continue
                if self.blank_unique_field(record, key):
                    continue
                self.not_blank_unique_field(record, key)

    def add_prod_association(self, record, key):
        '''
        add_prod_association is called from the create record loop AFTER all the main records
        (categories, groups, paragraphs and references) have been created.  Since part of the creation
        process is adding the prod_id to the record_lookup table, we can now find the association record
        using the foreign keys.

        1. use the dev_id to look up the prod_id for the foreign keys
        2. substitute the foreign keys and do a find
        4. If found, do nothing, else call the create record method
        '''
        record = self.find_associated_foreign_keys(record, key)
        res = self.find_wrapper(record, key)
        if not res['found']:
            self.do_prod_create(record, key)

    def find_associated_foreign_keys(self, record, key):
        '''
        find_associated_foreign_keys finds the prod ids for the association records

        :param record: association record
        :type record: dict
        :param key: key to the type of record
        :type key: str
        :return: association record with the prod ids substituted for the dev ids
        :rtype: dict
        '''
        record = self.substitute_prod_foreign_key(record, 'paragraph_id', 'paragraphs')
        if key == 'group_paragraph':
            return self.substitute_prod_foreign_key(record, 'group_id', 'groups')
        if key == 'paragraph_reference':
            return self.substitute_prod_foreign_key(record, 'reference_id', 'references')

    def blank_unique_field(self, record, key):
        '''
        blank_unique_field tests if the input record has a blank unique field.  This method drives the
        process if it does.  This should only happen in development.  The process is as follows:

        If development
           - create unique field (guid or slug)
           - add record to create list (with some modifications)
           - The fake id will behave like the dev_id for substitutions, therefore add it to
             self.record_lookups[top_key][unique_field] dictionary as dev_id)
           not here.....
           - Will substitute prod id after the new record is created (later on)

        If production, error out

        :param record: This is the input record, originally from development, manually updated
        :type record: dict
        :param key: This is the key from the input and also for some processing data
        :type key: str
        :return: True if there was a blank unique field and False if there was not
        :rtype: bool
        '''
        unique_field = crud.UPDATE_DATA[key]['unique_field']
        if methods.valid_non_blank_string(record[unique_field]):
            return False
        if self.input_data['is_prod']:
            sys.exit(f'Error! production environment, blank unique field in {record}')
        rec_to_create = self.add_unique_field(record, key, unique_field)
        self.add_fake_dev_ids_to_record_lookup(key, record['id'], record[unique_field])
        self.process_data[key]['create'].append(rec_to_create)
        return True

    def not_blank_unique_field(self, record, key):
        '''
        not_blank_unique_field does the followiing:
            1. Does a record lookup based on the unique field
            2. Not found in the development environment - error!
            3. Not found in the production environment - add record to the create list
            4. If found (production or development) - calls finalize_update_prep method
        :param record: dictionary form of the record to be created or updated
        :type record: dict
        :param key: [description]
        :type key: [type]
        :return: [description]
        :rtype: [type]
        '''
        res = self.find_wrapper(record, key)
        if not self.input_data['is_prod'] and not res['found']:
            message = ('Error! All development records in this method should already exist; '
                       'Input record == {res["record"]}')
            sys.exit(message)
        if res['found']:
            self.finalize_update_prep(record, key, res['record'])
        else:
            self.process_data[key]['create'].append(record)

    def finalize_update_prep(self, record, key, existing_record):
        '''
        finalize_update_prep does the following:
        1. If development, errors out if found id does not match the input id
           If production, substitutes the id in the input record with the id found in production
        2. Removes the 'created_at' field, so we do not over-write it
        3. Add it to the list of records that we will update
        4. Add the prod id to the lookup data

        :param record: [description]
        :type record: [type]
        :param key: [description]
        :type key: [type]
        :param existing_record: [description]
        :type existing_record: [type]
        '''
        if self.input_data['is_prod']:
            record['id'] = existing_record.id
        elif record['id'] != existing_record.id:
            message = ('Error! In development the found record id should match the existing record id'
                       f'existing record == {existing_record};  input record == {record}')
            sys.exit(message)
        record.pop('created_at', None)
        self.process_data[key]['update'].append(record)
        self.add_prod_id_to_record_lookup(record, key)

    def add_unique_field(self, record, key, unique_field):
        '''
        add_unique_field allows user to simply blank out the unique field during the manual step (see
        scripts/documentation/update_process.md) of updating records.  This is when using run_as_prod
        in the development environment to create new records.

        :param record: record that was created manually using the run_as_prod process
        :type record: dict
        :param key: key used to find the information necessary to run generic creates and updates
        :type key: str
        :param unique_field: key that is used to identify records, always unique for given db table
        :type unique_field: str
        :return: dictionary with necessary information to create a new record with run_as_prod method
        :rtype: dict
        '''
        if key == 'references':
            record[unique_field] = slugify(record['link_text'])
        elif key == 'paragraphs':
            record[unique_field] = uuid.uuid4()
        elif key in ('categories', 'groups'):
            record[unique_field] = slugify(record['title'])
        else:
            sys.exit(f'Error! Invalid key in add_unique_field, key == {key} & record == {record}')
        return record

    def create_record_loop(self):
        '''
        create_record_loop loops through the records that did not exist in the preprocessing and does
        the creates.

        * Note - assuming that the inner list will will be empty for associations, since they were not
                 preprocessed
        '''
        for key in crud.UPDATE_RECORD_KEYS:
            for record in self.process_data[key]['create']:
                if key in crud.ASSOCIATION_RECORD_KEYS:
                    self.add_prod_association(record, key)
                    continue
                self.do_prod_create(record, key)

    def do_prod_create(self, record, key):
        '''
        do_prod_create does the following:
         1. Assumes that the slug or guid do not exist on the db therefore does not do find
         2. creates a dictionary to use for input params for the create process
         3. Adds the newly created record to the prod results created list
         4. Adds the prod id to the record lookup, so that associated records can find the prod_id

        :param record: This is the input record obtained through db retrieval &/or manually updated
        :type record: dict
        :param key: key to information about model, so can be created successfully
        :type key: str
        '''
        class_ = crud.UPDATE_DATA[key]['class']
        create_dict = self.create_dict_from_record(record, key)
        record = self.create_record(class_, create_dict)
        record_dictionary = self.change_to_dict_or_error_out(record, create_dict)
        self.prod_results[key]['created'].append(record_dictionary)
        self.add_prod_id_to_record_lookup(record_dictionary, key)

    def add_prod_id_to_record_lookup(self, record, key):
        '''
        add_prod_id_to_record_lookup adds the prod id to the lookup table to make sure the
        association records are created with the correct foriegn keys

        :param record: record just created
        :type record: dict
        :param key: key to the record type that we created
        :type key: str
        '''
        if key == 'paragraphs':
            self.record_lookups[key][record['guid']]['prod_id'] = record['id']
        elif key not in crud.ASSOCIATION_KEYS:
            self.record_lookups[key][record['slug']]['prod_id'] = record['id']

    def create_dict_from_record(self, record, key):
        '''
        create_dict_from_record removes the id, created_at and update_at values, since they are
        all automatically created

        Does NOT remove the slug or guid because in the prod create process, they should already exist

        :param record: created manually if it's in development or through a retrieval process from
                       development if we are adding development data to production
        :type record: dict
        :return: data input to the generic create record process
        :rtype: dict
        '''
        record.pop('updated_at', None)
        record.pop('created_at', None)
        record.pop('id', None)
        if key == 'groups' and record['category_id'] is not None:
            record = self.substitute_prod_foreign_key(record, 'category_id', 'categories')
        return record

    def substitute_prod_foreign_key(self, record, record_key, top_level_key):
        '''
        substitute_prod_foreign_key finds the prod_id or the real dev_id for the run_as_prod process
        for the previously created category.  This will be used for the category_id in the group

        Since groups are the only records with a foriegn key field, so we named this method in a
        non-generic way.

        Two errors could be thrown.
        1. A Value Error if a fake dev id is not an integer
        2. A Key Error if there is no prod id for the given category in the lookup table

        :param record: record created manually when a record has foreign keys
        :type record: dict
        :return: group record with the production id (or real development id) added
        :rtype: dict
        '''
        str_dev_id = str(record[record_key])
        unique_field = self.record_lookups[top_level_key][str_dev_id]
        record[record_key] = self.record_lookups[top_level_key][unique_field]['prod_id']
        return record

    def update_record_loop(self):
        '''
        update_record_loop loops through the records that did not exist in the preprocessing and does
        the updates.

        * Note - assuming that the inner list will will be empty for associations, since they were not
                 preprocessed
        '''
        for key in crud.UPDATE_RECORD_KEYS:
            for record in self.process_data[key]['update']:
                self.do_prod_update(record, key)

    def do_prod_update(self, record, key):
        '''
        do_prod_updates does an update with the record was found by the unique field

        :param record: This is the original found record with the prod id
        :type record: dict
        :param key: key to the information necessary to do the generic find and update
        :type key: string
        '''
        unique_field = crud.UPDATE_DATA[key]['unique_field']
        class_ = crud.UPDATE_DATA[key]['class']
        find_dict = {unique_field: record[unique_field]}
        self.update_record(class_, record)
        updated_record = self.find_record(class_, find_dict)
        record_dictionary = self.change_to_dict_or_error_out(updated_record, find_dict)
        self.prod_results[key]['updated'].append(record_dictionary)

    def change_to_dict_or_error_out(self, record, info):
        '''
        change_to_dict_or_error_out if something is wrong with db update then get out as soon as possible
        Change the db model to a dictionary to enable association processing

        :param record: db record of model type
        :type record: projects.models.paragraphs object (Group for example)
        :param info: dictionary used to find or create the db object
        :type info: dict
        :return: dictionary form of projects.models.paragraphs object (Group for example)
        :rtype: dict
        '''
        if not record:
            sys.exit(f'Something happened with {record.__name__} create or update, info=={info}')
        if not isinstance(record, dict):
            record = record.__dict__
        return record

    def add_fake_dev_ids_to_record_lookup(self, top_key, dev_id, unique_field):
        '''
        add_fake_dev_ids_to_record_lookup allows ids fabricated in manual editing when running as
        prod in development.  If this was running in the production environment only, this method would
        not be needed.  The fake ids are used to link categories, paragraphs, groups and references with
        their associated records, since the development ids will not exist until the record is created

        :param top_key: valid top keys are in <UPDATE_RECORD_KEYS> (import constants.crud as crud)
        :type top_key: str
        :param key: primary id for the given record (fabricated while editing)
        :type dev_id: int
        :param value: unique field that is different from the primary key
        :type value: str
        '''
        try:
            str_key = str(dev_id)
        except ValueError:
            sys.exit(f'can not convert fake development id to string {dev_id}')
        self.record_lookups[top_key][str_key] = unique_field
        self.record_lookups[top_key][unique_field] = {'dev_id': dev_id}

    def find_wrapper(self, record, key):
        '''
        find_wrapper creates a dictionary to find the record and catches the record not found error
        returns a boolean found, indicating if the record is found and also the record if it is found

        :param key: key to find the information to identify record class and unique field
        :type key: string
        :param unique_field: unique field value
        :type unique_field: str
        :return: dictionary containing the boolean found, and the record
        :rtype: dict
        '''
        output = {'found': False, 'record': record}
        if key in crud.ASSOCIATION_RECORD_KEYS:
            find_dict = self.dictionary_to_find_association_records(record, key)
        else:
            field_name = crud.UPDATE_DATA[key]['unique_field']
            find_dict = {field_name: record[field_name]}

        try:
            output['record'] = self.find_record(crud.UPDATE_DATA[key]['class'], find_dict)
        except crud.UPDATE_DATA[key]['class'].DoesNotExist:
            return output
        output['found'] = True
        return output

    def dictionary_to_find_association_records(self, record, key):
        '''
        dictionary_to_find_association_records creates the dictionary needed in the find method to
        find an existing association method

        :param key: key from input data used to find process data
        :type key: str
        :param record: record retrieved from JSON input, may or may not exist on database
        :type record: dict
        :return: the dictionary used to find the database record corresponding to the input record
        :rtype: dict
        '''
        unique_fields = crud.CREATE_DATA[f'add_{key}']['unique_fields']
        find_dict = {}
        for field in unique_fields:
            find_dict[field] = record[field]
        return find_dict

    def add_delete_associations_to_prod_results(self):
        for key in crud.ASSOCIATION_RECORD_KEYS:
            if len(self.process_data[key]['delete']) > 0:
                if key in self.prod_results.keys():
                    self.prod_results[key]['delete'] = self.process_data[key]['delete']
                else:
                    self.prod_results[key] = {'delete': self.process_data[key]['delete']}


