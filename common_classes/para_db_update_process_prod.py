'''
    This is Step Three of the database update process, but for production.  Step 1 retrieves data &
    Step 2 edits the data.  If this is truly production & not testing, Step 2 will be skipped
'''

import sys
import pprint
from decouple import config
from common_classes.para_db_update_process import ParaDbUpdateProcess
import constants.crud as crud
import utilities.random_methods as utils
from utilities.record_dictionary_utility import RecordDictionaryUtility


class ParaDbUpdateProcessProd(ParaDbUpdateProcess):
    '''
        ParaDbUpdateProcessProd will be run for updates in production.  The only reason for this class
        to run in another environment is for testing.  All data should match development data, since
        development is the source of truth.

        ParagraphReference and GroupParagraph both use ids, so we need to have a lookup table
        (self.record_lookups) to find the production ids using the pargraph guids and (reference or
        group slugs)
    '''

    def __init__(self, input_data, updating):
        '''
            __init__ stores the input data & provides some additional framework for processing.
        '''
        super().__init__(input_data, updating)
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
            if config('ENVIRONMENT') == 'production':
                sys.exit(crud.RECORD_LOOKUP_MESSAGE_PROD)
            else:
                sys.exit(crud.RECORD_LOOKUP_MESSAGE_DEV)

    def process_input_data_update_db(self):
        '''
            process_input_data_update_db is the main driver of the update process.  You can see the order
            that we process the data by the method names.
        '''
        if self.only_delete:
            self.deleting_associations()
            sys.exit('Exiting after only deleting associations')

        self.validate_input_keys()
        self.preliminary_record_setup()
        if not self.updating:
            print('-----------------Process Data-------------------------------')
            printer = pprint.PrettyPrinter(indent=1, width=120)
            printer.pprint(self.process_data)
            print('------------------Lookup Data-------------------------------')
            printer = pprint.PrettyPrinter(indent=1, width=120)
            printer.pprint(self.record_lookups)
            return
        self.create_record_loop()
        self.update_record_loop()
        self.deleting_associations()

    def deleting_associations(self):
        '''
            We need to explicitly delete associations using the unique key lookups for paragraph
            guids and (reference or group slugs).  If we already deleted them in development, they
            can not be retrieved in Step 1, to be part of self.file_data.
        '''
        self.add_or_delete_associations()
        # print('-------------------Process Data----------------------------------')
        # printer = pprint.PrettyPrinter(indent=1, width=120)
        # printer.pprint(self.process_data)
        print('------------------prod_results-----------------------------------')
        printer = pprint.PrettyPrinter(indent=1, width=120)
        self.move_delete_info_to_prod_results()
        printer.pprint(self.prod_results)

    def validate_input_keys(self):
        '''
            validate_input_keys validates input keys.  There is only one validation left.

            For this application, the devlopment database is the source of truth.  The input data for
            production should always be retrieved from development (db_update_S1, with for_prod argument)

            ParaDbUpdateProcessProd fails when there are explicit_creates (not based on existing data)
        '''
        if self.explicit_creates():
            data = self.file_data
            sys.exit(f'Input error: explicit creates prohibited in production: {data}')

    def explicit_creates(self):
        '''
            explicit_creates validates that we do not do explicit creates; that is why we have
            ParaDbUpdateProcess, which can not run in production.  The only reason we do not prohibit
            this class in other environments is to test, therefore keep everything as much the same as
            possible.

            :return: returns True when there are input keys like add_*
            :rtype: bool
        '''
        return utils.dictionary_key_begins_with_substring(self.file_data, 'add_')

    def preliminary_record_setup(self):
        '''
            preliminary_record_setup will loop through input data and set up the data in two ways:
            1. Non-association records - need to add the production ids to the lookup table
            2. Always adds association records to the create list, because until all the parent records
               are created, we will not be able to find the ids necessary for associations
        '''
        for key in crud.UPDATE_RECORD_KEYS:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            self.prod_results[key] = {'created': [], 'updated': []}
            for record in self.file_data[key]:
                if key in crud.ASSOCIATION_RECORD_KEYS:
                    self.process_data[key]['create'].append(record)
                    continue
                self.unique_field_lookup(record, key)

    def add_prod_association(self, record, key):
        '''
            add_prod_association is called from the create record loop AFTER all the main records
            (categories, groups, paragraphs and references) have been created.  Since part of the
            creation process is adding the prod_id to the record_lookup table, we can now find the
            association record using the foreign (parent) keys.

            1. use the dev_id to look up the prod_id for the foreign keys
            2. substitute the foreign guid or slug and do a find
            3. If found, do nothing for paragraphreference, but update the grouppargraph record,
               because the order field (to order paragraphs within a group) may need updating
            4. Otherwise, call the create record method
        '''
        record = self.find_associated_foreign_keys(record, key)
        res = self.find_wrapper(record, key)
        if not res['found']:
            self.do_prod_create(record, key)
            return
        if key != 'group_paragraph':
            return
        params = self.update_group_paragraph_params(record, key)
        print(f'params=={params}')
        self.update_group_paragraph_order(**params)

    def update_group_paragraph_params(self, record, key):
        '''
        update_group_paragraph_params returns params needed to update_group_paragraph_order

        :param record: contains the value to update and the data needed to find the correct record
        :type record: dict
        :param key: used to know which record we are updating or creating
        :type key: str
        :return: parameters needed by para_db_methods to update the order field
        :rtype: dict
        '''
        return {
            'key': key,
            'group_id': record['group_id'],
            'paragraph_id': record['paragraph_id'],
            'order': record['order']
        }

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

    def unique_field_lookup(self, record, key):
        '''
        unique_field_lookup (of non-association records) does the followiing:
            1. Does a record lookup based on the unique field
            2. Not found in the development environment - error! (may eventually allow this in test)
            3. Not found in the production environment - add record to the create list
            4. If found (production or development) - calls finalize_update_prep method
        :param record: dictionary form of the record to be created or updated
        :type record: dict
        :param key: corresponds to a top level key in self.file_data.  Use to know db record type
        :type key: string
        '''
        self.validate_for_prod_prep(record, key)
        res = self.find_wrapper(record, key)
        if config('ENVIRONMENT') == 'development' and not res['found']:
            message = ('Error! All development records in this method should already exist; '
                       f'Input record == {res["record"]}')
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
            4. Add the prod id to the lookup data, so that later on association records can be created or
            updated

            :param record: Originally retrieved from the development environment (self.file_data)
            :type record: dict
            :param key:  corresponds to a top level key in self.file_data.  Use to know db record type
            :type key: str
            :param existing_record: existing record that was found
            :type existing_record: dict(?)
        '''
        if config('ENVIRONMENT') == 'production':
            record['id'] = existing_record.id
        elif record['id'] != existing_record.id:
            message = ('Error! In development the found record id should match the existing record id'
                       f'existing record == {existing_record};  input record == {record}')
            sys.exit(message)
        record.pop('created_at', None)
        self.process_data[key]['update'].append(record)
        self.add_prod_id_to_record_lookup(record, key)

    def create_record_loop(self):
        '''
            create_record_loop loops through the records that did not exist in the preprocessing and does
            the creates.

            crud.UPDATE_RECORD_KEYS lists the association keys last, so the parent records should always
            exist at this point
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
        elif key not in crud.ASSOCIATION_RECORD_KEYS:
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
            substitute_prod_foreign_key finds the production id for the foreign keys in the association
            records.  For example, group_id and paragraph_id in the GroupParagraph record

            Two errors could be thrown, theoretically, but it would mean a programming mistake in Step 1.
            1. A Value Error if a dev id is not an integer
            2. A Key Error if there is no prod id for the given category in the lookup table

            :param record: record created manually when a record has foreign keys
            :type record: dict
            :return: group record with the production id (or, for testing test id) added
            :rtype: dict
        '''
        str_dev_id = str(record[record_key])
        unique_field = self.record_lookups[top_level_key][str_dev_id]
        if utils.key_not_in_dictionary(self.record_lookups[top_level_key][unique_field], 'prod_id'):
            self.assign_existing_record_prod_id(top_level_key, str_dev_id)
        record[record_key] = self.record_lookups[top_level_key][unique_field]['prod_id']
        return record

    def assign_existing_record_prod_id(self, top_level_key, dev_id):
        '''
            assign_existing_record_prod_id finds the existing record, so if there are any associated the
            prod id can be substituted

            :param top_level_key: top level key for main record (paragraphs, groups, etc)
            :type top_level_key: str
            :param dev_id: str dev id used as key in lookup table for the given record to be associated
            :type dev_id: str
        '''
        unique_key = crud.UPDATE_DATA[top_level_key]['unique_field']
        class_name = crud.UPDATE_DATA[top_level_key]['class']
        unique_value = self.record_lookups[top_level_key][dev_id]
        record = self.find_record(class_name, {unique_key: unique_value})
        queryset = RecordDictionaryUtility.get_content(class_name, record.id)
        self.add_prod_id_to_record_lookup(queryset[0], top_level_key)

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
            change_to_dict_or_error_out changes the record to dictionary format to enable association
            processing.  If record is None, processing stops.

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

    def find_wrapper(self, record, key):
        '''
            find_wrapper finds the record associated with the given keys.  It uses constants to
            enable generic code.

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

        if output['record'] != find_dict:
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

    def move_delete_info_to_prod_results(self):
        '''
        move_delete_info_to_prod_results calls the same process to delete associations as exists
        in the normal update process.  This moves the generated documentation to prod_results,
        so we can see what happened
        '''
        for key in crud.ASSOCIATION_RECORD_KEYS:
            if len(self.process_data[key]['delete']) > 0:
                if key in self.prod_results.keys():
                    self.prod_results[key]['delete'] = self.process_data[key]['delete']
                else:
                    self.prod_results[key] = {'delete': self.process_data[key]['delete']}

    def validate_for_prod_prep(self, record, key):
        '''
        validate_for_prod_prep ensures before any updates that all non-association records that have
        a unique key also have and entry in the record lookup

        Exits the system if there is a key error
        '''
        if key in crud.ASSOCIATION_RECORD_KEYS:
            return
        print('----------------------Record Lookups----------------------------')
        try:
            unique_field = self.record_lookups[key][str(record['id'])]
            print(f'successfully looked up record with unique_key == {unique_field}')
        except KeyError:
            if config('ENVIRONMENT') == 'production':
                sys.exit(crud.RECORD_LOOKUP_MESSAGE_PROD)
            else:
                sys.exit(crud.RECORD_LOOKUP_MESSAGE_DEV)
