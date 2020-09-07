# Update Process for Development and Eventually Production
## Three Step Process
1. Prepare input and run scripts/batch_json_db_updater_s1.py
    - note - usage documented in run method
2. Start with Step 1 output data and edit what you want updated and delete the rest
3. Run batch_json_db_updater_s3 to update the database using the Step 2 file changes

## Distinction between run_as_prod and is_prod
* important note - it is possible to use run_as_prod to create new data, but if you start with existing data and do not explicitely create new unique fields it would be easy to over-write existing data.  That would be a pain, and if things were automated, could be even a bigger pain to make right.
- run_as_prod parameter is only development & only step 3 (see details below)
- is_prod - if run_as_prod is True OR if it's the production environment
- Input parameter, run_as_prod, used to update development like production.  Used for testing and as an alternate way to make updates
- Designed to work with updated_at
- Deleting associations work identically in development and production, therefore are a little different

## Details
- Note - exact paths are in constant variables: constants/scripts.py

1. Step 1 Json Input process (run_as_prod == False in Step 3):
    - Copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
    - Delete the "updated_at" key and value
    - You may need to run some preliminary db queries or put in some print statements to get ids, guids, etc
    - Choose one or zero retrieval keys: "group_ids", "category_ids", "paragraph_ids", The array of ids will be used as a where statement that will pull in all the associated data so it can be edited.
    - Important fact: you will get TypeError unless the ids are strings; although ids are ints on the db, in this process we are converting the data to a query string
    - It is possible to create zero, one or more reference(s), group(s), categor(ies/y) (Can also associate the new category with a new group).
      These creates are the only database changes that happen in Step 1.
    - Associations can also be added and deleted, the example json indicates how, but the input will only be copied to the Step Three Input
    - Open scripts/batch_json_db_updater_s1.py and use the Step One Usage examples
    - Step One output will be written to the <MANUAL_UPDATE_JSON> directory
 2. Step 2.  Edit the file produced by Step 1 (still with run_as_prod == False).
    - Will be in <MANUAL_UPDATE_JSON> directory
    - For updating records, always leave the unique keys:
    --> ids (always), guid for paragraphs, and slug for references, categories and groups.
    --> other than that, you only need the field(s) you are updating
    - If a record is not being updated, just delete it and save some run-time
    - When you are done editing, move the file to <INPUT_TO_UPDATER_STEP_THREE>
 3. Step 3. Open scripts/batch_json_db_updater_s3.py and follow the Step Three Usage Instructions
    - After running, the program will copy the delete_associations input dictionary to the <PROD_INPUT_JSON> directory
    - delete_associations dictionaries are identical in development and production input
 4. run_as_prod instructions
    - Do the following in Step One to find the input data for updating development like production:
        1. In step one
           * Same copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
           * If you use the "updated_at" key and value, the output file for Step 1 (input to Step 3) will get the the correct prefix for run_as_prod programmatically (otherwise file will be ignored when run_as_prod is used unless you manually update the filename).
           * **The only key you can use along with updated_at, is delete_association** (Otherwise it gets too kludgy, because run_as_prod is acting as if the records already exist in development.  Creates are done implicitly in production (& run_as_prod), whereas in the normal development updates, the creates for categories, groups and references are always explicit and it is impossible to create paragraphs in development using the update process.)
           * Whatever input you use, the program will pull in data that you have already created in development.
           * For run_as_prod in development, the prefix must be <PROD_PROCESS_IND>
           * After editing the file in the <MANUAL_UPDATE_JSON> directory, make sure the prefix is correct and move to <INPUT_TO_UPDATER_STEP_THREE> for run_as_prod in development.
           * If we were really running in production, we would automatically move the file to <PROD_INPUT_JSON> after doing Step One with updated_as and delete_associations as the only keys.  If I like using the run_as_prod option, I may want to create a run_as_prod script argument at that time, to avoid confusion.

        2. In step two - edit the run_as_prod input data
           * Will be in <MANUAL_UPDATE_JSON> directory
           * To do an update to existing data, just update the data as normal, but keep all the data intact.
           * To create new records (replacing most of the existing data you pulled), do the following:
              1. Create unique keys (**slug for groups**, categories or references; **guid** for paragraphs).
              2. Edit the ids for all records to be unrealistically high (higher than anything existing)
              3. Be sure to match the corresponding foreign ids in the association records.
           * **Not editing all of the steps:  1, 2 & 3 (directly above) correctly could mess up existing data badly!**
           * If updating with run_as_prod in development or updating in the production environment,
             when the data is not found by the unique key, the program will create new data
             (including paragraphs) and substitute the real id into any relationships
        3. The files will need to have <PROD_PROCESS_IND> (value of) as a prefix to the json filename
          - The <PROD_PROCESS_IND> (value of) as a prefix to the json filename will be added to the filename programatically if you use the updated_at input dictionary in Step One.  You will need to move the file to the the <PROD_INPUT_JSON> directory manually.
          - Anytime delete_associations are done in development, the exact same input dictionary will be created in the the <PROD_INPUT_JSON> directory.  This should happen programmatically and the prefix will be .
4. To update production, do this in Step 1 & 2:
    - Copy (don't move) this template to data/data_for_updates/dev_input
    - Do the following in Step One to find the input data for updating production:
        1. Pull in data using the updated_at date/time input
           * This is the ONLY input you should ever have for a update production run
           * There should not be any other create or edit possibilities
           * Real production updates should happen without manual intervention.  The manual steps are only because we are writing new content.
        2. If you are confident, just assume the data is correct and move the file from <MANUAL_UPDATE_JSON>
           to the <PROD_INPUT_JSON> directory
        3. If you are not confident, just go back to steps 1 & 2 and edit the data and run the db updates
           in development first
        4. This could be automated, if it ever becomes cumbersome.
        5. Deleting associations in production is simply a matter of moving the dictionary input that has the delete_association key to the the <PROD_INPUT_JSON> directory.  This will happen programmatically, which will be a pain before there actually is a production.