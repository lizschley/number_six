''' This is Step Three of the database update process.  Step 1 retrieves & Step 2 edits the data '''

import sys
from decouple import config
import constants.crud as crud
import constants.scripts as scripts
import helpers.no_import_common_class.paragraph_helpers as helpers
import utilities.random_methods as utils
import utilities.json_methods as json_helper
from common_classes.para_db_methods import ParaDbMethods


class ParaDbUpdateProcess(ParaDbMethods):
    '''
        ParaDbUpdateProcess updates or creates data based on self.file_data, which is created by
        ParaDbUpdatePrep (running scripts/db_updater_s1.py creates self.file_data, see it for details).

        ParaDbUpdateProcess's main purpose is to update existing data, preserving the relationships.

        For development - The only way to create paragraphs is through ParaDbCreateProcess.  The create
                          process also creates a paragraph's related records

                        ParaDbUpdateProcess allows you to create any records besides a paragraph

                        In fact, categories can only be created in the update process, since they are
                        not directly related to paragraphs

        For production - All updates use ParaDbUpdateProcessProd, which inherits this process.
                         If you try to use this class for production, if should error out

    '''

    def __init__(self, input_data, updating):
        '''
            __init__ stores the input data and provides the necessary framework to process the input data

            :param input_data: This is generally a file produced by ParaDBUpdatePrep and then manually
                               updated.
            :type input_data: dict
            :param updating: if this parameter does not exist, there will be no db updates
            :type updating: bool
            '''
        super().__init__(updating)
        self.file_data = input_data.pop('file_data')
        self.script_data = input_data
        # import pprint
        # printer = pprint.PrettyPrinter(indent=1, width=120)
        # printer.pprint(f'script_data == {self.script_data}')
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
        self.check_environment()
        self.create_record_loop()
        self.update_record_loop()
        if self.updating:
            self.add_or_delete_associations()
        # import pprint
        # printer = pprint.PrettyPrinter(indent=1, width=120)
        # printer.pprint(self.process_data)

    def check_environment(self):
        '''
            Exit with error message if this is run in the production environment
        '''
        if config('ENVIRONMENT') == 'production':
            sys.exit(f'Input error: wrong process for production: script_data: {self.script_data}')

    def create_record_loop(self):
        '''
            create_record_loop finds or creates the record, based on the keys in the input data.
            It loops through the CREATE_RECORD_KEYS to know which keys to look for and hen calls the
            find or create wrapper method with the necessary arguments to do the actual find or create
            CRUD.
        '''
        for key in crud.CREATE_RECORD_KEYS:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            for record in self.file_data[key]:
                self.find_or_create_wrapper(key, record)

    def update_record_loop(self):
        '''
            update_record_loop finds and updates the record, based on the keys in the input data.
            It loops through the UPDATE_RECORD_KEYS to know which keys to look for and then calls the
            find_and_update_wrapper method with the necessary arguments to do the actual find and update
            CRUD.
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
        if len(unique_fields) == 1:
            self.assign_to_process_data(top_level_key, self.ensure_dictionary(class_, record),
                                        unique_fields[0], 'create', found)

    def ensure_dictionary(self, class_, record):
        '''
            ensure_dictionary makes sure the record is in dictionary format

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
            input key as add_categories, then categories is the top key, and the assignment is a
            dictionary that has the unique key value pointing to the record created.  This ensures we do
            not create duplicate records and that the record created information is available

            :param top_key: this is the input data key (originally from a JSON file)
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
        if key == 'paragraphs':
            record = self.associate_ref_para(record)

        unique_field = crud.UPDATE_DATA[key]['unique_field']
        class_ = crud.UPDATE_DATA[key]['class']
        find_dict = {unique_field: record[unique_field]}
        returned_record = self.find_and_update_record(class_, find_dict, record)

        if utils.key_in_dictionary(returned_record, 'error'):
            sys.exit(returned_record['error'])

        self.assign_to_process_data(key, self.ensure_dictionary(class_, returned_record),
                                    unique_field, 'update', True)

    def associate_ref_para(self, para):
        '''
            associate_ref_para initiates the process of turning the list of references' slug or
            link_text to associations between a given paragraph and all of its references

            :param para: one paragraph
            :type para: dict
        '''
        if utils.no_keys_from_list_in_dictionary(('ref_slug_list', 'link_text_list'), para):
            return para

        if utils.key_not_in_dictionary(self.file_data, 'add_paragraph_reference'):
            self.file_data['add_paragraph_reference'] = []

        add_para_refs = helpers.initiate_paragraph_associations(para,
                                                                self.correct_ref_data(para.keys()),
                                                                self.file_data['add_paragraph_reference'])
        if add_para_refs is not None:
            self.file_data['add_paragraph_reference'] = add_para_refs
        para = utils.pop_keys(('ref_slug_list', 'link_text_list'), para)
        return para

    @staticmethod
    def correct_ref_data(keys):
        ''' return the necessary information to assign the the list of references to the para'''
        return crud.PARA_GUID_REF_SLUG if 'ref_slug_list' in keys else crud.PARA_GUID_REF_LINK_TEXT

    def add_category_to_group(self, group_to_create):
        '''
            add_category_to_group allows adding a category id to a group before updating the group

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
                json_helper.write_dictionary_to_file(self.file_data[input_key],
                                                     prefix=scripts.PROD_PROCESS_IND,
                                                     directory_path=scripts.PROD_INPUT_JSON)
            elif function == 'add':
                self.add_associations(input_key, input_dictionaries)

    def add_associations(self, input_key, create_dict_list):
        '''
            add_associations makes it possible to create a many to many association between group and
            paragraph OR paragraph and reference.  This does not get called until the association data
            is prepared by looking up the parent data using unique keys.  The parent record information
            is substituted in the create_dict

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
            is prepared by looking up the parent data using unique keys.  The parent record information
            is substituted in the find_dict

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
            if rec == 'link_text':
                data['unique_fields'] = [rec]
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
        unique_field = association_data['unique_fields'][0]
        input_key = 'link_text' if unique_field == 'link_text' else association_key + '_' + unique_field
        unique_value = input_dict[input_key]
        record = self.find_record(association_data['class'], {unique_field: unique_value})
        create_field_name = association_key + '_id'
        return {create_field_name: record.id}

    def current_association_key(self, association_from_input):
        '''
            current_association_key parses the input for the given record.  All we need is the first
            part, since it is the key to the ASSOCIATION_DATA, which is used by both add and delete
            associations to find the class and the unique field to find the object

            :param association_from_input: key to ASSOCIATION_DATA parsed from input data
            :type association_from_input: dict
            :return: the specific key needed in to obtain the data needed
            :rtype: str
        '''
        if association_from_input == 'link_text':
            return 'reference'
        info = utils.dict_from_split_string(association_from_input, '_', ['association_key'])
        return info['association_key']
