# Update Process for Development and Eventually Production
## Three Step Process
1. Prepare input and run scripts/db_updater_s1.py
    - note - usage documented in run method
2. Start with Step 1 output data and edit what you want updated and delete the rest
3. Run db_updater_s3 to update the database using the Step 2 file changes


## Distinction between running in development and running in production

The normal create process for development is to use the scripts/create_paragraphs.py.  This process will never run in production, however.  In production we only load data retrieved from development, understanding the primary keys (automatically created ids) may be different.

**Step 1 with for_prod parameter**
This simply creates the file with the prod prefix.  Production input is designed to skip Step 2 (the manual step) entirely

**Step 3 with for_prod parameter**
In order to test the production process, I created the for_prod parameter.  This is a pain to actually use and adds more room for error that could be hard to recover from.

Here are the three danger areas:
1. If you want to pull existing data and over-write it to make new data, it is vital to make empty strings of the unique key (slug or guid).  If you don't, the process could easiy over-write data you started with (identifies records with unique keys).
2. If you create new data and associate it to other records using fake ids (see below for more details), it is totally necessary to make sure the file does not have any  existing associations with the fake ids.  If you pull in data of the same record type that you are creating and that data has associated data with the same ids, you could associate the wrong records to your newly created ones.
3. Also if you run Step One - the file created will have a date in the file name.  The program will sort descending on that date, so keep that in mind.  The order can make a difference.  It's better to run Step 1 again and cut and paste your updates (from the messed up file), rather than run against data that has been updated after you did your data retrieval.

**End Note**

## Running in development vs running in production -- continued
- <CAPITAL_LETTERS_IN_ANGLE_BRACKETS> indicates a [constant](https://github.com/lizschley/number_six/blob/develop/constants/scripts.py).
- Step 1 will never run in production, because development is the source of truth.
- Preparing to run in the actual production environment and preparing to for_prod in developmment, are the same in in Step One
- In production, the assumption is that the data was already created in development.  For that reason, we pull the data from the development database and move the file to production and write the data to production (without editing, eventually plan to automate this process).  This is an **implicit create**.  Whereas in development, using the normal create and update processes, the data that is loaded can legitimately be new data.  This is an **explicit create**.  If we are running with the for_prod script argument, however we are pretending to do implicit creates, even though it is really brand new data.  Basically, for_prod fakes out the system.
- The script argument, for_prod, is used programatically to update development in the same way as production.  It was originally designed for testing before there was a production environment, but has evolved as an alternate way to make updates.  It definitely requires manual editing, since otherwise we would be writing back the exact same data.
- By using for_prod as an argument in Step 1, you will not be able to use the wrong input, for example, it forbids using the explicit [create keys](https://github.com/lizschley/number_six/blob/develop/data/json_templates/updating_dev_input_template.json) (JSON keys beginning with add_) as input and also adds the <PROD_PROCESS_IND> prefix to the file output to the <INPUT_TO_UPDATER_STEP_THREE> directory
- for_prod and real production in Step 3 forbids the explicit creates (key beginning with add_) and will only read json files that are named correctly.
- Deleting associations work identically in development and production, therefore the input is the same.
- It does not throw an error if you are trying to delete the same associations multiple times (as long as the records with the foreign keys still exist).
- No matter how you delete associations, deleting associations automatically writes a file to the production update input directory.  The file contents are exactly like the input for deleting associations in development and the filename has the production prefix.
- It is also possible to delete associations along with the normal for_prod input.

## Step by step process
1. Step 1 Json Input process (for_prod == False):
    - If you need to simply update one record or type of record and you are not changing any relationships, there is a bypass:
      1. Create an argument as follows:
         - Use one of the top level keys in <UPDATE_DATA> (constants.crud)
         - Add an equal sign
         - Add a list of ids **1,2,3** with no spaces OR add the word **all**
         - This will copy all of the data needed to start the update to the <INPUT_TO_UPDATER_STEP_THREE> directory
         - Follow the Step 2 and Step 3 process as normal
         - For example: **paragraphs=80,86**
         - Another example: **categories=all**
      2. This does not give you any relational data.
      3. Normally follow the Step One process described below.
    - Copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
    - Choose zero or more retrieval keys: "group_ids", "category_ids", "paragraph_ids", or "updated_at"
      1. The array of ids or updated_at will be used in a where statement that will pull in all the associated data so it can be edited.
      2. It is necessary to do this data retrieval, before doing updates.
      3. It could be helpful to do one of the following:
         * Run preliminary db queries
         * Run step 1 seperately to get the information needed and delete the manual json after getting what you need
         * Do inspect element when looking at data on dev web server
         * Put in some print statements to get ids, guids, etc
    - Open scripts/db_updater_s1.py and use the Step One Usage examples
    - Step One output will be written to the <INPUT_TO_UPDATER_STEP_THREE> directory
    - The add_* keys and the delete_* keys will automatically be copied over to the output file and the only reason to change the values would be to use the information retrieved in Step One to add the information or to make corrections.
 2. Step 2.  Edit the file produced by Step 1 (still with for_prod == False).
    - Will be in <INPUT_TO_UPDATER_STEP_THREE> directory
    - For updating records, always leave the unique keys:
    --> ids (always), guid for paragraphs, and slug for references, categories and groups.
    --> other than that, you only need the field(s) you are updating
    - If an existing record is not being updated, it is ok to delete it.
    - When you are done editing, move the file to <INPUT_TO_UPDATER_STEP_THREE>
 3. Step 3. Open scripts/db_updater_s3.py and follow the Step Three Usage Instructions
    - Any actual db change (create, update, delete) happens in Step 3
    - After running, the program will copy the delete_associations input dictionary to the <PROD_INPUT_JSON> directory
    - delete_associations dictionaries are identical in development and production input
 4. for_prod OR Production Process
    - Do the following in Step One to find the input data for updating development like production:
        1. In step one
           * Copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
           * Use for_prod parameter
              1. This gives you the correct output filename
              2. Prod (whether real production or for_prod) creates a lookup table that is necessary in order to update associations
                 - If you are adding associations, the foreign record dictionaries (Paragraphs, References, Group and/or Category) must be in the original retrieval, in order for Step 1 to programmatically create the lookup table (associating unique key and dev_id).
                 - In step 2, you can delete the foreign record dictionary, but leave the information in the lookup table
                 - It will never hurt to have too much in the lookup table, so there is not a good reason to edit it.  You can, obviously, manually update it, but the less manual work the better.
              3. Program will error out if you try to do explicit creates (keys begin with add_*).
                 - Otherwise it gets too kludgy, because for_prod is acting as if the records already exist in development.
                 - Creates are done implicitly in production (& for_prod), whereas in the normal development, the creates for categories, groups and references are always explicit and it is impossible to create paragraphs in development using the update process.
           * **Delete_association works in all situations**  It works the same in production and development whether using for_prod or not
           * Whatever input you use, the program will pull in data that you have already created in development.
           * For for_prod in development (or for production), the prefix will automatically be <PROD_PROCESS_IND>
        2. In step two (for for_prod in development) - edit the for_prod input data (no editing for production)
           * Will be in <INPUT_TO_UPDATER_STEP_THREE> directory
           * To do an update to existing data, just update the data as normal like you do for normal development updating
           * To create new records (can do at the same time you are updating some data)
              1. Do a data retrieval, making sure to have at least one existing record dictionary of the type (paragraph, group, etc) you are creating.
              2. Either cut and paste an existing record dictionary or simply edit one that you do not need to update.
              3. Blank out the unique keys (**slug** for groups, categories or references; and **guid** for paragraphs).
              4. The primary key (id) MUST match the foreign keys in the association records and MUST NOT be used in other records in the file.
                  - Therefore make a fake id that is not being used elsewhere (really high, needs to be int or string that can become int)
                  - Make sure that the same ID is not used to update an existing record and also create a new record (will mess up associations).
                  - Using non-numerics will cause a Value Error
                  - Associations are as follows: groupparagraph, paragraphreference and also the category id in the group record
                  - To create associations for existing records, you need to have retrieved the main record (Paragraphs, References, Group and/or Category),so that the lookup table will have the unique keys necessary.  It is not necessary, however. to keep the main record in the Step 3 input, unless you have updates you want to perform.
              5. Make sure to carefully check the following, matching the corresponding foreign ids in the association records:
                  - category_id in the group record
                  - group_id and paragraph_id in the group_paragraph record
                  - paragraph_id and reference_id in the paragraph_reference record
              6. Do not worry about the lookup table when creating new paragraphs, references, groups and/or categories.  That is only for existing records.
           * **DANGER** - not following through all of the steps: 1-6 (directly above) correctly could mess up existing data!
           * If creating new records with for_prod in development, the program will create unique keys explicitly (so that the update process mimics production, without the work of manually creating the keys)
           * If in the production environment, blank unique keys will cause the program to error out.
           * After editing the file in the <INPUT_TO_UPDATER_STEP_THREE> directory, make sure the prefix is correct and move to <INPUT_TO_UPDATER_STEP_THREE> for for_prod in development.
           * Once we have a production environment, it will be a decision to move the file to <PROD_INPUT_JSON>, except for deleting associations, which aleady write to <PROD_INPUT_JSON>.  Have not yet developed an automation process, plan to run manually often first.
        3. In Step 3 - process to make database creates and association updates
           - There is a lookup table that will only be created when you run the step one script with the for_prod script argument
           - The <PROD_PROCESS_IND> (value of) prefix will have been added to the filename programatically when using for_prod runtime argument in Step One.
           - You will still need to move the file to the the <INPUT_TO_UPDATER_STEP_THREE> directory manually.
           - When the data is not found by the unique key (won't even look in development, since the unique keys are freshly created), the program will create new data (including paragraphs) and substitute the real id into any relationships
           - Anytime delete_associations are done in development, the exact same input dictionary will be created in the the <PROD_INPUT_JSON> directory.  This should happen programmatically and the prefix will be the value of the <PROD_PROCESS_IND>.
4. To update production, do this in Step 1 & 2:
    - Same copy (don't move) data/json_templates/updating_dev_input_template.json to <INPUT_TO_UPDATER_STEP_ONE>
    - The goal is to automate this entire process.  There should be NO manual updates at all!
    - Do the following in Step One to find the input data for updating production:
        1. Retrieve data in the normal way.  The updated_at input key was created for production runs.
           * Retrieve the records that were edited on development.  Use the for_prod script argument.
           * Data with these keys should run, unchanged, on production: 'delete_paragraph_reference', 'delete_group_paragraph'.  This will happen automatically whenever an association is deleted: output will be written to the <PROD_INPUT_JSON>  directory.
           * Real production updates should happen without manual intervention.  The manual steps are only because we are writing new content.
        2. If you are confident, just assume the data is correct and move the file from <INPUT_TO_UPDATER_STEP_THREE>
           to the <PROD_INPUT_JSON> directory (Maybe we should always move it automatically)... later decision
        3. If you are not confident, just go back to steps 1 & 2 and edit the data and run the db updates
           in development first

## Development Environment Notes
- Adds, creates and deletes ONLY happen in Step 3, but... you can write the following input JSON in <INPUT_TO_UPDATER_STEP_ONE>
   1. Add new standalone records, keys are as follows: 'add_categories', 'add_references', 'add_groups' (not for_prod)
   2. Add new Associations, keys are as follows: 'add_paragraph_reference', 'add_group_paragraph' (not for_prod)
   3. Delete existing Associations, keys are as follows: 'delete_paragraph_reference', 'delete_group_paragraph' (always works the same)
- The program will automatically copy the add_ dictionaries and the delete_ dictionaries to the output file from Step 1 (read below for further details).
- If you don't need to update any existing records, you can skip Step 1 entirely.  **However**, running step 1 can be helpful to retrieve the information necessary to add new records or delete associations.  But if you have what you need, just copy example from data/json_templates/updating_dev_input_template.json directly to <INPUT_TO_UPDATER_STEP_THREE>, make the updates you want and delete the following keys: 'updated_at','group_ids','category_ids','paragraph_ids' (those are for the retrievals necessary for updating and can only be done in Step 1)
