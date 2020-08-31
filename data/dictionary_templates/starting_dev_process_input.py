'''
    Use this as a template for the dictionary input to the data retrieval before updates

    To update development, do this in Step 1:
       * Copy (don't move) this template to data/data_for_updates/dev_input
       * Fill in or delete the main key and values
       * Can only update existing paragraphs, unless updating production or running as prod (see below)
       * For running as prod (in development), need to experiment a lot to make sure that
         we give good directions, particularly for associations.  It should be possible
         to do any creates this way if it is more convenient that the normal create

    To update development with same method as production (run_as_prod), do this in Step 1 & 2:
        * Copy (don't move) this template to data/data_for_updates/dev_input
        * Do the following in Step One to find the input data for updating production:
        1. In step one - Pull in data using the updated_at date/time input
           * This will pull in data that you have already created in development
           * There should not be any other create or edit possibilities

        2. In step two - edit this data to do an update to existing data or create new records
           * To edit existing data, simply edit the records, in this case the program will do an lookup
             based on the unique keys find it and then do an update as opposed to a create
           * If you want to create new data, you need to explicitly create unique keys for the
             records you want to create:
                 paragraph: guids
                 categories, groups or references: slugs
           * Set the id way higher than anything existing
           * Be careful to use the matching ids in associations
           * If updating with run_as_prod in development or updating in the production environment,
             when the data is not found by the unique key, the program will create new data and
             substitute the real id into any relationships
        3. The files will need to have <PROD_PROCESS_IND> (value of) as a prefix to the json filename
           This should be added to the create output file in Step One

    To update production, do this in Step 1 & 2:
        * Copy (don't move) this template to data/data_for_updates/dev_input
        * Do the following in Step One to find the input data for updating production:
        1. Pull in data using the updated_at date/time input
           * This is the ONLY input you should ever have for a update production run
           * There should not be any other create or edit possibilities
        2. If you are confident, just assume the data is correct and move the file in dev_manual input
           to the the prod_input directory
        3. If you are not confident, just go back to steps 1 & 2 and edit the data and run the db updates
           in development first
        4. This could be automated, if it ever becomes cumbersome
'''
import os
import portfolio.settings as settings
from projects.models.paragraphs import Category


BLOG = Category.CATEGORY_TYPE_CHOICES[0][0]
RESUME = Category.CATEGORY_TYPE_CHOICES[1][0]
FLASH_CARD = Category.CATEGORY_TYPE_CHOICES[2][0]


INPUT_TO_DEV_UPDATER = {
    # See production and run_as_prod notes above
    # if updated_at has a date, then any other input is an error.  Only for updating production
    #    or creating new data in development with the same techniques (basically faking out the system)
    #    see above documentation for details
    'updated_at': None,

    'add_categories': [{}, ],
    'add_references': [{}, ],
    'add_groups': [{'title': '', 'note': '', 'category_id': None,
                    'category_title': ''}, ],
    'delete_associations': [{'paragraph_id': 0, 'reference_id': 0}, {'group_id': 0, 'paragraph_id': 0}],
    'add_associations': [{'paragraph_guid': '', 'reference_slug': ''}, ],

    # One of the following (delete others, including 'updated_at'):
    'group_ids': [],
    'category_ids': [],
    'para_ids': [],

    # can override if you understand the process and have a reason
    'output_directory': os.path.join(settings.BASE_DIR, 'data/data_for_updates/dev_manual_json/'),
}

# the following is only for convenience, so I can cut and paste original format and then update
EXAMPLE_INPUT = {
    # See production and run_as_prod notes above
    # if updated_at has a date, then any other input is an error.  Only for updating production
    #    or creating new data in development with the same techniques (basically faking out the system)
    #    see above documentation for details
    'updated_at': None,

    # The following creates are done in Step 1, but all other db creates or updates will be in step 2
    # If the data already exists, will NOT update.  To update, need use the
    'add_categories': [{'title': 'Reverse Chronological Resume', 'type': RESUME},
                       {'title': 'Functional Resume', 'type': RESUME}],
    'add_references': [{'link_text': '', 'url': ''}],
    'add_groups': [{'title': 'QA Automation', 'note': '', 'category_id': None,
                    'category_title': 'Functional Resume'}, ],

    # These won't happen until step 3, don't want to add or delete the association before updating the
    # paragraph
    'delete_associations': [{'paragraph_id': 4, 'reference_id': 8}, {'group_id': 5, 'paragraph_id': 43}],
    'add_associations': [{'paragraph_guid': 'valid paragraph guid', 'reference_slug': 'valid ref slug'},
                         {'group_slug': 'valid group slug', 'paragraph_guid': 'valid paragraph guid'}],

    # Choose only ne of the following (also can't be updated_at):
    'reference_ids': [],
    'group_ids': [],
    'category_ids': [],
    'para_ids': [],

    # can override if you understand the process and have a reason
    'output_directory': os.path.join(settings.BASE_DIR, 'data/data_for_updates/dev_manual_json/'),
}
