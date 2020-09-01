# Update Process for Development and Eventually Production
## Three Step Process
1. Prepare input and run scripts/batch_json_db_updater_s1.py
    - note - usage documented in run method
2. Start with Step 1 output data and edit what you want updated and delete the rest
3. Run batch_json_db_updater_s3 to update the database using the Step 2 file changes

## Definition: run_as_prod
There is a input parameter called run_as_prod in the Step 3 Script.  This is used to update development
like production.  You need to know ahead of time when this is the technique you are using, because
updated_at is the only json input that you can use.  The program will error out if you try to combine
it with other possibilities. More details below

## Details
- Note - exact paths are in constant variables: constants/scripts.py

1. Step 1 Json Input process when run_as_prod will be false in Step 3:
    - Copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
    - Delete the "updated_at" key and value
    - You will need to run some db queries to get ids, guids, etc
    - Choose one or none of the following keys: "group_ids", "category_ids", "reference_ids", ""  The array of ids will be used as a where statement that will pull in all the associated data so it can be edited.
    - It is possible to add reference, groups, categories (also can associate the new category with a group).  These creates are the only database changes that happen in Step 1.  You can add as many as you want.
    - Associations can also be added and deleted, the example json indicates how.
    - Fill in the values or delete the main key and values from the input, don't leave empty keys
    - Once the input file is edited and and in the correct directory, follow the usage directrions to run step 1
    - The file to actually do the updates in will be in the <MANUAL_UPDATE_JSON> directory

2. Step 2.  Edit the file produced by Step 1 (still with run_as_prod == False).
    - Should be in <MANUAL_UPDATE_JSON> directory (can override default)
    - Make edits you want to make
    - If a record is not being updated, just delete it and save some run-time
    - When you are done, move the file to <INPUT_TO_UPDATER_STEP_THREE>

3.  To update development with same method as production (run_as_prod), do this in Step 1 & 2:
    - Copy (don't move) this template to data/data_for_updates/dev_input
    - Do the following in Step One to find the input data for updating production:
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
             when the data is not found by the unique key, the program will create new data
             (including paragraphs) and substitute the real id into any relationships
        3. The files will need to have <PROD_PROCESS_IND> (value of) as a prefix to the json filename
           This should be added to the create output file in Step One (Plan to do this automatically)

4. To update production, do this in Step 1 & 2:
    - Copy (don't move) this template to data/data_for_updates/dev_input
    - Do the following in Step One to find the input data for updating production:
        1. Pull in data using the updated_at date/time input
           * This is the ONLY input you should ever have for a update production run
           * There should not be any other create or edit possibilities
        2. If you are confident, just assume the data is correct and move the file from <MANUAL_UPDATE_JSON>
           to the the <PROD_INPUT_JSON> directory
        3. If you are not confident, just go back to steps 1 & 2 and edit the data and run the db updates
           in development first
        4. This could be automated, if it ever becomes cumbersome