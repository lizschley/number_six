# Update Process for Development and Eventually Production
## Three Step Process
1. Prepare input and run scripts/batch_json_db_updater_s1.py
    - note - usage documented in run method
2. Start with Step 1 output data and edit what you want updated and delete the rest
3. Run batch_json_db_updater_s3 to update the database using the Step 2 file changes

**Aside -**
This is separate from the normal create process: scripts/batch_json_processor.py.  In the process that is being documented here, the only way you can create paragraphs is with the run_as_prod method, though there is a way to explicitly create any other paragraph records.

## Distinction between running in development and running in production
### Also running in development as if it were production (run_as_prod)
**important note** - it is possible to use run_as_prod to create new data, but if you start with existing data and do not make empty strings of the unique key (slug or guid), the process could easiy over-write existing data.  That would be a pain, and if things were automated, could be even a bigger pain to make right.  Read on for more details.
- <CAPITAL_LETTERS_IN_ANGLE_BRACKETS> indicates a [constant](https://github.com/lizschley/number_six/blob/develop/constants/scripts.py).
- Step 1 will never run in production, because development is the source of truth.
- Preparing to run in the actual production environment and preparing to run_as_prod in developmment, are the same in in Step One
- In production, the assumption is that the data was already created in development.  For that reason, we pull the data from the development database and move the file to production and write the data to production.  This is an **implicit create**.  Whereas in development, the data that is loaded can legitimately be new data.  This is an **explicit create** unless we are running with the run_as_prod script argument.
- The script argument, run_as_prod, is used programatically to update development in the same way as production.  It was originally designed for testing before there was a production environment, but has evolved as an alternate way to make updates
- By using run_as_prod as an argument in Step 1, you will not be able to use the wrong input, for example, it forbids using the explicit [create keys](https://github.com/lizschley/number_six/blob/develop/data/json_templates/updating_dev_input_template.json) (JSON keys beginning with add_) as input and also adds the <PROD_PROCESS_IND> prefix to the file output to the <MANUAL_UPDATE_JSON> directory
- run_as_prod and real production in Step 3 forbids the explicit creates (key beginning with add_) and will only read json files that are named correctly.
- Deleting associations work identically in development and production, therefore the input is the same

## Details
- Adds, creates and deletes ONLY happen in Step 3, but... you can write the following input JSON in <INPUT_TO_UPDATER_STEP_ONE>
   1. Add new standalone records, keys are as follows: 'add_categories', 'add_references', 'add_groups' (not run_as_prod)
   2. Add new Associations, keys are as follows: 'add_paragraph_reference', 'add_group_paragraph' (not run_as_prod)
   3. Delete existing Associations, keys are as follows: 'delete_paragraph_reference', 'delete_group_paragraph' (always works the same)
- The program will automatically copy the add_ dictionaries and the delete_ dictionaries to the output file from Step 1 (read below for further details).
- If you don't need to update any existing records, you can skip Step 1 entirely.  Just copy example from data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_THREE> and delete the following keys: 'updated_at','group_ids','category_ids','paragraph_ids' (those are for the retrievals necessary for updating and can only be done in Step 1)

1. Step 1 Json Input process (run_as_prod == False):
    - Copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
    - Choose one or zero retrieval keys: "group_ids", "category_ids", "paragraph_ids", or "updated_at"
      1. The array of ids or updated_at will be used in a where statement that will pull in all the associated data so it can be edited.
      2. It is necessary to do this data retrieval, before doing updates.
      3. You may need to run some preliminary db queries, run step 1 just to get the information needed or put in some print statements to get ids, guids, etc
      4. **Important fact:** you will get a TypeError unless the ids are strings; although ids are ints on the db, in this process we are converting the data to a query string
    - Open scripts/batch_json_db_updater_s1.py and use the Step One Usage examples
    - Step One output will be written to the <MANUAL_UPDATE_JSON> directory
    - The add_* keys and the delete_* keys will automatically be copied over to the output file and the only reason to change the keys or values would be to make corrections.
 2. Step 2.  Edit the file produced by Step 1 (still with run_as_prod == False).
    - Will be in <MANUAL_UPDATE_JSON> directory
    - For updating records, always leave the unique keys:
    --> ids (always), guid for paragraphs, and slug for references, categories and groups.
    --> other than that, you only need the field(s) you are updating
    - If a record is not being updated, just delete it and save some run-time
    - When you are done editing, move the file to <INPUT_TO_UPDATER_STEP_THREE>
 3. Step 3. Open scripts/batch_json_db_updater_s3.py and follow the Step Three Usage Instructions
    - Any actual db change (create, update, delete) happens in Step 3
    - After running, the program will copy the delete_associations input dictionary to the <PROD_INPUT_JSON> directory
    - delete_associations dictionaries are identical in development and production input
 4. run_as_prod OR Production Process
    - Do the following in Step One to find the input data for updating development like production:
        1. In step one
           * Same copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
           * Use run_as_prod parameter
              1. This will give you the correct output filename & will error out if you try to do explicit creates (keys begin with add_*).
              2. Otherwise it gets too kludgy, because run_as_prod is acting as if the records already exist in development.  Creates are done implicitly in production (& run_as_prod), whereas in the normal development, the creates for categories, groups and references are always explicit and it is impossible to create paragraphs in development using the update process.
           * **You CAN use the delete_association key**  This is exactly the same in production and development
           * Whatever input you use, the program will pull in data that you have already created in development.
           * For run_as_prod in development, the prefix will automatically be <PROD_PROCESS_IND>
        2. In step two (for run_as_prod in development) - edit the run_as_prod input data (no editing for production)
           * Will be in <MANUAL_UPDATE_JSON> directory
           * To do an update to existing data, just update the data as normal like you do for normal development updating
           * To create new records (replacing most of the existing data you pulled), do the following:
              1. Blank out the unique keys (**slug** for groups, categories or references; and **guid** for paragraphs).
              2. The primary keys will be ignored, EXCEPT they must match the primary keys in the association records.  Also you need to make sure that the same ID is not used to update an existing record and also create a new record (will mess up associations).
                  - category_id in the group record
                  - group_id and paragraph_id in the group_paragraph record
                  - paragraph_id and reference id in the paragraph_reference record
              3. Be sure to match the corresponding foreign ids in the association records.
           * **DANGER** - not following through all of the steps:  1, 2 & 3 (directly above) correctly could mess up existing data badly!
           * If creating new records with run_as_prod in development, the program will create unique keys explicitly (so that the update process mimics production, without the work of manually creating the keys)
           * If in the production environment, blank unique keys will cause the program to error out.
           * After editing the file in the <MANUAL_UPDATE_JSON> directory, make sure the prefix is correct and move to <INPUT_TO_UPDATER_STEP_THREE> for run_as_prod in development.
           * Once we have a production environment, it will be a decision to move the file to <PROD_INPUT_JSON>.  Not sure yet how to automate.
        3. In Step 3 - process to make database updates
          - There is a lookup table that will only be created when you run the step one script with the run_as_prod script argument
          - The <PROD_PROCESS_IND> (value of) prefix will have been added to the filename programatically when using run_as_prod runtime argument in Step One.
          - You will still need to move the file to the the <INPUT_TO_UPDATER_STEP_THREE> directory manually.
          - When the data is not found by the unique key (won't even look in development, since the unique keys are freshly created), the program will create new data (including paragraphs) and substitute the real id into any relationships
          - Anytime delete_associations are done in development, the exact same input dictionary will be created in the the <PROD_INPUT_JSON> directory.  This should happen programmatically and the prefix will be the value of the <PROD_PROCESS_IND>.
4. To update production, do this in Step 1 & 2:
    - Same copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
    - The goal is to automate this entire process.  There should be NO manual updates at all!
    - Do the following in Step One to find the input data for updating production:
        1. Retrieve data in the normal way.  The updated_at input key was created for production runs.
           * Retrieve the records that were edited on development.  Use the run_as_prod script argument.
           * Data with these keys should run, unchanged, on production: 'delete_paragraph_reference', 'delete_group_paragraph'.  This will happen automatically whenever an association is deleted: output will be written to the <PROD_INPUT_JSON>  directory.
           * Real production updates should happen without manual intervention.  The manual steps are only because we are writing new content.
        2. If you are confident, just assume the data is correct and move the file from <MANUAL_UPDATE_JSON>
           to the <PROD_INPUT_JSON> directory (Maybe we should always move it automatically)... later decision
        3. If you are not confident, just go back to steps 1 & 2 and edit the data and run the db updates
           in development first
