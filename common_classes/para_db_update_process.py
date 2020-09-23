''' This is Step Three of the database update process.  Step 1 retrieves & Step 2 edits the data '''

import sys
import pprint
import constants.crud as crud
import helpers.no_import_common_class.utilities as utils

from common_classes.para_db_methods import ParaDbMethods


class ParaDbUpdateProcess(ParaDbMethods):
    '''
        ParaDbUpdateProcess updates (or if production or run_as_prod, creates) data based on
        self.input_data
    '''

    def __init__(self, input_data, updating):
        '''
        __init__ stores the input data and provides the necessary framework to process the input data

        :param input_data: This is generally a file produced by ParaDBUpdatePrep and then manually
        updated.  There are a lot of variations, see documentation:
        :type input_data: [type]
        :param updating: [description]
        :type updating: [type]
        '''
        super(ParaDbUpdateProcess, self).__init__(updating)
        self.file_data = input_data.pop('file_data')
        self.input_data = input_data
        # print(f'input_data == {self.input_data}')
        self.process_data = {'updating': self.updating,
                             'categories': {'existing': [], 'create': [], 'update': []},
                             'groups': {'existing': [], 'create': [], 'update': []},
                             'references': {'existing': [], 'create': [], 'update': []},
                             'paragraphs': {'existing': [], 'create': [], 'update': []},
                             'group_paragraph': {'create': [], 'update': [], 'delete': []},
                             'paragraph_reference': {'create': [], 'update': [], 'delete': []},
                             }

    def process_input_data_update_db(self):
        '''
        process_input_data_update_db is the main driver of the update process.  You can see the order
        that we process the data by the method names.
        '''
        self.validate_input_keys()
        self.create_record_loop(crud.CREATE_RECORD_KEYS, self.file_data)
        self.update_record_loop()
        self.add_or_delete_associations()
        printer = pprint.PrettyPrinter(indent=1, width=120)
        printer.pprint(self.process_data)

    def validate_input_keys(self):
        '''
        validate_input_keys ensures that the user (me) is doing careful work

        It runs some tests on the input keys and errors with a message, if the tests fail
        '''
        if self.incorrect_environment():
            data = self.file_data
            sys.exit(('Input error: wrong process for development unless running as prod: '
                      f'input_data: {self.input_data}, file_data: {data}'))

    def incorrect_environment(self):
        '''
        incorrect_environment ensures that the given environment matches the process used

        :return: returns True if you are running this process in production or running as prod
        :rtype: bool
        '''
        if self.input_data['is_prod'] or self.input_data['run_as_prod']:
            return True
        return False

    def create_record_loop(self, keys, input_data):
        '''
        create_record_loop finds or creates the record, based on the keys in the input data.  It loops
        through the CREATE_RECORD_KEYS to know which keys to look for and hen calls the find or create
        wrapper method with the necessary arguments to do the actual find or create CRUD.

        :param keys: constants of the keys we use to do the explicit creates
        :type keys: tuple of strings
        :param input_data: the input data, now a dictionary (originally JSON file)
        :type input_data: dict
        '''
        for key in keys:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            for record in input_data[key]:
                self.find_or_create_wrapper(key, record)

    def update_record_loop(self):
        '''
        update_record_loop finds and updates the record, based on the keys in the input data.  It loops
        through the UPDATE_RECORD_KEYS to know which keys to look for and then calls the
        find_and_update_wrapper method with the necessary arguments to do the actual find and update
        CRUD.

        :param keys: constants of the keys we use to do the updates
        :type keys: tuple of strings
        :param input_data: the input data, now a dictionary (originally JSON file)
        :type input_data: dict
        '''
        for key in crud.UPDATE_RECORD_KEYS:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            for record in self.file_data[key]:
                self.find_and_update_wrapper(key, record)

    def find_or_create_wrapper(self, key, record):
        '''
        find_or_create_wrapper prepares the input data to use the generic crud methods

        :param key: input key from input data (now key to dictionary was once JSON key)
        :type key: string
        :param record: model.Model class
        :type record: Model
        '''
        unique_fields = crud.CREATE_DATA[key]['unique_fields']
        class_ = crud.CREATE_DATA[key]['class']
        temp = key.split('_', 1)
        top_level_key = temp[1] if len(temp) == 2 else key
        find_dict = {}
        for field in unique_fields:
            # print(f'in for, field == {field}, record == {record}')
            find_dict[field] = record[field]
        create_dict = self.add_category_to_group(record) if key == 'add_groups' else record
        returned_record = self.find_or_create_record(class_, find_dict, create_dict)
        found = returned_record['found']
        record = returned_record['record']
        # Todo: find_or_create/in ParaDbMethods: find print output and update return type documentation
        print(f'Need to update find or create with correct return type: {type(record)} ')
        if len(unique_fields) == 1:
            self.assign_to_process_data(top_level_key, self.ensure_dictionary(class_, record),
                                        unique_fields[0], 'create', found)

    def ensure_dictionary(self, class_, record):
        '''
        ensure_dictionary creates a dictionary from the returned record if it is not already a dictionary

        :param class_: model class that was found or created
        :type class_: model.Model
        :param record: The instance of the model created or found OR the create dict record
        :type record: model.Model or dictionary
        :return: dictionary form of the record that was created
        :rtype: dict
        '''
        if record.__class__.__name__ == class_.__name__:
            return record.__dict__
        return record

    def assign_to_process_data(self, top_key, record, unique_field, action=None, found=True):
        '''
        assign_to_process_data takes the record created and assigns it to the correct key (say if the
        input key as add_categories, then categories is the top key, and the assignment is a dictionary
        that has the unique key value pointing to the record created.  This ensures the we do not try
        to create duplicate records and that the record created information is available

        :param key: this is the input data key (originally from a JSON file)
        :type key: string
        :param record: This is the record created or a dictionary representation of that record
        :type record: model.Model or dictionary
        :param unique_field: field name for the unique key (besides id) for the given record
        :type unique_field: str
        '''
        if action is not None:
            self.process_data[top_key][action].append(record)
        if top_key in ('group_paragraph', 'paragraph_reference'):
            return
        record_key = record[unique_field]
        if found or record.get('id'):
            self.process_data[top_key]['existing'].append({record_key: record})

    def find_and_update_wrapper(self, key, record):
        '''
        find_and_update_wrapper finds the record based on the information in the UPDATE_DATA constant
        with the given key

        :param key: key used to find the UPDATE_DATA information
        :type key: [str
        :param record: dictionary representation of the record to be found or created
        :type record: dict
        '''
        unique_field = crud.UPDATE_DATA[key]['unique_field']
        class_ = crud.UPDATE_DATA[key]['class']
        find_dict = {unique_field: record[unique_field]}
        # Todo: find_and_update/in ParaDbMethods: find print output and update return type documentation
        returned_record = self.find_and_update_record(class_, find_dict, record)

        print(f'Need to update find & update with correct return type: {type(returned_record)} ')
        if utils.key_in_dictionary(returned_record, 'error'):
            sys.exit(returned_record['error'])

        self.assign_to_process_data(key, self.ensure_dictionary(class_, returned_record),
                                    unique_field, 'update', True)

    def add_category_to_group(self, group_to_create):
        '''
        add_category_to_group makes it so you can add a category id to a group before updating the group

        :param group_to_create: dictionary used to create a group
        :type group_to_create: dict
        :return: updated group to create (no category_title and category_id equal to  None or int)
        :rtype: dict
        '''
        cat_title = group_to_create.pop('category_title', '')
        if not cat_title:
            return self.pop_cat_id_if_zero(group_to_create)
        cat_list = self.process_data['categories']['existing']
        if not cat_list:
            return self.pop_cat_id_if_zero(group_to_create)
        cat = utils.find_value_from_dictionary_list(cat_list, cat_title)
        if self.updating:
            group_to_create['category_id'] = cat[0]['id']
        else:
            group_to_create['category_id'] = 99
        return group_to_create

    def pop_cat_id_if_zero(self, group_to_create):
        '''
        pop_cat_id_if_zero replaces a zero with a None (null category field)  This only gets called
        when there is no category to associate with the given group

        :param group_to_create: group dictionary (create_dict) with no associated category
        :type group_to_create: dict
        :return: dict with None as the category id (postgres null)
        :rtype: dict
        '''
        if group_to_create['category_id'] == 0:
            group_to_create.pop('category_id', None)
        return group_to_create

    def add_or_delete_associations(self):
        '''
        add_or_delete_associations starts the process of reading data from the add and delete
        associations portion of the input data.  This will be used when you want to associate a
        paragraph with another group, for example.  Usually adding a reference will be done in a
        normal update, but if you just forgot to add a reference, this is an easy fix.

        This is called only in Step 3 since it involves changing data in the database

        Throughout much of this process we have constants that drive the input data, directing to
        the correct process
        '''
        for input_key in crud.ASSOCIATION_KEYS:
            if utils.key_not_in_dictionary(self.file_data, input_key):
                continue
            function, data_key = input_key.split('_', 1)

            input_dictionaries = self.prepare_association_data(self.file_data[input_key], data_key)
            if function == 'delete':
                self.delete_associations(data_key, input_key, input_dictionaries)
            elif function == 'add':
                self.add_associations(input_key, input_dictionaries)

    def add_associations(self, input_key, create_dict_list):
        '''
        add_associations makes it possible to create a many to many association between group and
        paragraph OR paragraph and reference.  This does not get called until the association data
        is prepared, unique keys are used to look up data and the ids are substituted in the create_dict

        :param input_key: would be add_paragraphreference or add_groupparagraph
        :type input_key: str
        :param create_dict_list: list of all the add associations for the given key
        :type create_dict_list: list
        '''
        # print(f'create_dict_list: {create_dict_list}')
        for create_dict in create_dict_list:
            self.find_or_create_wrapper(input_key, create_dict)

    def delete_associations(self, data_key, input_key, find_dict_list):
        '''
        delete_associations makes it possible to delete a many to many association between group and
        paragraph OR paragraph and reference.  This does not get called until the association data
        is prepared, unique keys are used to look up data and the ids are substituted in the create_dict

        The same process will be used in production, so after the association is deleted, the
        delete_association data will be written to a file in the prod input directory

        :param input_key: would be delete_paragraphreference or delete_groupparagraph
        :type input_key: str
        :param create_dict_list: list of all the delete associations for the given key
        :type create_dict_list: list
        '''
        class_to_delete = crud.DELETE_ASSOCIATIONS[input_key]['class']
        for find_dict in find_dict_list:
            self.assign_to_process_data(data_key, find_dict,
                                        None, 'delete', True)
            self.delete_record(class_to_delete, find_dict)

    def prepare_association_data(self, file_input_list, data_key):
        '''
        prepare_association_data takes the file input (which is a list) from the input file:
           data/data_for_updates/dev_input_step_three directory

        It also uses data from constants from constants/crud.py:
           ASSOCIATION_KEY
           ASSOCIATION_DATA
           CREATE_DATA

        The final result is a find or create on the association create dictionary

        :param input_key: key from input json: found in data/data_for_updates/dev_input_step_three
        :type input_key: str
        :param data_key: last part of the input_key is the key to ASSOCIATION_DATA constant
        :type data_key: str
        '''
        input_dictionaries = []
        for file_input in file_input_list:
            input_dictionaries.append(self.dict_from_foreign_associations(file_input, data_key))
        return input_dictionaries

    def dict_from_foreign_associations(self, foreign_key_records, data_key):
        '''
        dict_from_foreign_associations reads the input file and finds the two foreign associations
        (input_data), using the following format to find the foreign key records to associate
        groups with paragraphs or paragraphs with references.
        Here are two foreign key input_data examples:
        1.  [{"paragraph_guid": "a3575efb-e443-48da-89d7-20f8c5910229",
              "reference_slug": "unclebobmartincleancodeprogrammerspeakerteacher"}]
        2.  [{"group_slug": "functional-resume",
              "paragraph_guid": "21028615-1e01-4444-acc9-e581637e460b"}]

        Number 1 usage - For the paragraph_reference it finds the Paragraph using the guid and the
                         Reference using the slug.
        Number 2 usage - For the group_paragraph association, if finds the Group from the group slug
                         and the Paragraph from the paragraph guid.

        Once it finds the records, it gets the id to create the return dictionary

        example of return: {'paragraph_id': 9, 'reference_id': 9}

        :param foreign_key_records: dictionary from the input data (from json file mentioned earlier)
        :type foreign_key_records: dict
        :param data_key: key obtained from parsing input_data key.  Used to find ASSOCIATION_DATA
        :type data_key: str
        :return: dictionary that is used to create or delete the new association record
        :rtype: dict
        '''
        association_data = crud.ASSOCIATION_DATA[data_key]
        create_dict = {}
        for rec in foreign_key_records:
            association_key = self.current_association_key(rec)
            input_dict = {rec: foreign_key_records[rec]}
            data = association_data[association_key]
            create_dict.update(self.one_create_key_and_value(input_dict, association_key, data))
        return create_dict

    def one_create_key_and_value(self, input_dict, association_key, association_data):
        '''
        one_create_key_and_value takes the input record and the ASSOCIATION_DATA and puts it together
        to find one of the foreign records (Group, Paragraph or Record) so we use the key value pair,
        for example: {'paragraph_id': 9}

        :param input_dict: unique key information to find the foreign key parts of the association record
        :type input_dict: dict
        :param association_key: string
        :type association_key: used to find the necessary information to do the database lookups
        :param association_data: Constants used to understand the associations
        :type association_data: dict
        :return: one key value pair that is part of the data needed to create the association record
        :rtype: dict
        '''
        # input_dict == {'paragraph_guid': 'para_guid_r_a', 'reference_slug': 'ref_slug_a'}
        # or input_dict == {'group_slug': 'group_slug_a', 'paragraph_guid': 'parag_guid_g_a'}
        # association_data[key] = {'unique_fields': ['guid'], 'class': Paragraph} for example
        unique_field_name = association_data['unique_fields'][0]
        input_key = association_key + '_' + unique_field_name
        unique_value = input_dict[input_key]
        record = self.find_record(association_data['class'], {unique_field_name: unique_value})
        create_field_name = association_key + '_id'
        return {create_field_name: record.id}

    def current_association_key(self, association_from_input):
        '''
        current_assoication_key parses the input for the given record.  All we need is the first
        part, since it is the key to the ASSOCIATION_DATA, which is used by both add and delete
        associations to find the class and the unique field to find the object

        :param association_from_input: key to ASSOCIATION_DATA parsed from input data
        :type association_from_input: dict
        :return: the specific key needed in to obtain the data needed
        :rtype: str
        '''
        info = utils.dict_from_split_string(association_from_input, '_', ['association_key'])
        return info['association_key']
