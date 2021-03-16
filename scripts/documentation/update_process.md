# Create and Update Development and Production Data
## Development vs Production
For this portfolio application, the development data is the source of truth.  If the production site came down, the site will still be available in its entirety in development.  In development, data is created explicitly. In production, on the other hand, data is only created or updated when it already exists in development and is not orphaned.  For example, if you create a group and it is not associated with a paragraph, it will not be uploaded to the production database.  Because we rely on the associations that are originally created in development, the development and production data load processes are quite different.

The goal, however, is the same.  Creates, retrievals, updates and deletions (besides research and writing) should be easy.
## Record Types
1. Paragraphs - the main unit for the text that is displayed dynamically on the site
2. Groups - describe (to the application) how the paragraphs are to be displayed
3. References - show where the information comes from.  One exception, if the reference is not online, the information will be directly associated with the paragraph using the text field
4. GroupParagraph - associates a paragraph with a Group.  This is a many-to-many relationship.  Sometime paragraphs are ordered within a given group.  For that reason, there is order field in the GroupParagraph record.
5. ParagraphReference - associates a paragraph with a reference.  It is also a many-to-many relationship
6. Category - associates one category with many groups.  Groups can be ordered using the cat_sort field in the group record.
## Creating Paragraph Data in Development
The normal create process runs only in development.  It will throw an error if you try to run it in production.  The script is [create_paragraphs](https://github.com/lizschley/number_six/blob/develop/scripts/create_paragraphs.py) and corresponds to a class [para_db_create_paragraphs](https://github.com/lizschley/number_six/blob/develop/common_classes/para_db_create_process.py). The input data is in json format and uses this [create para template](https://github.com/lizschley/number_six/blob/develop/data/crud_input_templates/create_input.json). Using this template, you can create a group with multiple associated paragraphs.  You can also create many references or simply associate the new paragraphs with existing references.

The paragraph creation is for one group at a time and the script will fail unless a group can be found or created. Each paragraph within a "paragraphs" list will be automatically associated with the one group.  If the group already exists, the create process only needs the 'group_title' to find and associate the group with each paragraph in the list. If the group is found, the program will ignore any other group fields. You can also create a new group through this process.  See the template for more details.

Sometimes paragraphs within a group are ordered.  This will happen programmatically, based on the paragraph order in the input data's paragraphs list.

Reference / paragraph associations are automatically set up using a "link_text_list": [] within each paragraph.  If one reference is associated with multiple paragraphs, the reference's link_text field must be in the link_text_lists for multiple paragraphs.
## Updates in Development
Paragraphs are treated differently in the development process, because of their complexity. They contain most of the text and all of the html formatting, paths to images, css classes used to display those images and information to create various kinds of links during the paragraph display process.  The only way to create new paragraphs is by using [ParaDbCreateProcess](https://github.com/lizschley/number_six/blob/develop/common_classes/para_db_create_process.py)ParaDbCreateProcess (see above).

The development database update process uses the following three scripts [db_updater_s1](https://github.com/lizschley/number_six/blob/develop/scripts/db_updater_s1.py), [db_updater_s2](https://github.com/lizschley/number_six/blob/develop/scripts/db_updater_s3.py) and [db_change_order](https://github.com/lizschley/number_six/blob/develop/scripts/db_change_order.py) which contain usage information, and the [ParaDbUpdate](https://github.com/lizschley/number_six/blob/develop/common_classes/para_db_update_process.py) class and children classes.

- You can create the following records using the db_update process: category, group, reference, group_paragraph and paragraph_reference
- You can update the following records using the db_update process: paragraph, category, group, reference and group_paragraph
- You can delete the following records using the db_update process: group_paragraph and paragraph_reference
### Step One
The first step for updating records is to retrieve the existing records, and usually the related data. This is step one. Here is the template: [Step 1 input data](https://github.com/lizschley/number_six/blob/develop/data/crud_input_templates/update_input.json).  If you want to retrieve orphan records, you need to use input parameters, the documentation is in the script: [argument format: key=comma-delimited-ids](https://github.com/lizschley/number_six/blob/develop/scripts/db_updater_s1.py)

When you run the script, it will loop through the json files in the <INPUT_TO_UPDATER_STEP_ONE> directory [see script constants](https://github.com/lizschley/number_six/blob/develop/constants/scripts.py) Some commonly used inputs in the [Step 1 save directory](https://github.com/lizschley/number_six/tree/develop/data/data_for_updates/dev_input_step_one/save). You can simply move it to its parent directory and change the values to what you need.

Step One is only for data retrievals.  It instantiates [ParaDbUpdatePrep](https://github.com/lizschley/number_six/blob/develop/common_classes/para_db_update_prep.py) and runs its methods, which make do NOT make changes to the database.

However, the [Step One input](https://github.com/lizschley/number_six/blob/develop/data/crud_input_templates/update_input.json) includes formats for explicit creates (the add_* dictionary templates). These are not actually used in Step One, but will be copied over to the output automatically.  If you are only doing explicit creates, and do not need to retrieve a slug or a guid, there is no reason to run Step One.
### Step Two
Step One writes the data it retrieves to the the <INPUT_TO_UPDATER_STEP_THREE> directory [see script constants](https://github.com/lizschley/number_six/blob/develop/constants/scripts.py) directory.  Step 2 is the manual editing phase. It not necessary to delete data that does not need to be updated, but it looks cleaner and may make it easier.
### Step Three
Once the data is modified, run [db_updater_s3](https://github.com/lizschley/number_six/blob/develop/scripts/db_updater_s3.py). It includes usage information, such using or not using the updating argument.

Step Three processes these (unordered) top-level json keys first: finding or creating records in this order:
1. 'add_categories'
2. 'add_groups'
3. 'add_references'

Then it finds and updates records with these top-level keys, in this order:
1. 'categories'
2. 'references'
3. 'paragraphs'
4. 'groups'
5. 'paragraph_reference'
6. 'group_paragraph'

The order is important, because groups have a category_id which depends on the category already being created.  Association records can not be created, unless both the parent records exist.

Any error will stop the script.  The process is not entirely idempotent, because paragraphs can be duplicated.  Mistakes are rare, easy to recover from, and always (so far) due to carelessness, generally in the input data.
### In Practice
1. Explicit Creates - Groups can be created as part of the planning process. It is often easier to create groups and references ahead of time using the the updater, as opposed to during the create process.  It varies with the complexity and planned format of the data being created.
2. Update single records - often, all of the other records are set, but the wording is not right.  For that reason, you can get just paragraphs by sending in paragraphs=4,5,6 for example, where 4, 5 & 6 are paragraph ids.  This brings only the paragraphs. You can do this for groups or categories as well, in case you have an orphan group you would like to edit, for example.  The directions for this is in [db_updater_s3](https://github.com/lizschley/number_six/blob/develop/scripts/db_updater_s3.py). You can edit this [sql to get ids](https://github.com/lizschley/number_six/blob/develop/originals/sql/list_of_comma-delimited_ids.sql).
3. Tag Helper - html tags are stored in the paragraph records.  Often I type this directly in the json file.  But for complex html coding, it is helpful to use a [helper](https://github.com/lizschley/number_six/blob/develop/helpers/tag_finisher.html) so that vscode will complete the tags and the html and be tested ahead of time.
4. Static Files - all the static files (css, js and images) are on S3.  The css and js are versioned, so that caching is not an issue. To make this process more convenient, use the [s3_updater script](https://github.com/lizschley/number_six/blob/develop/scripts/s3_updater.py)that compiles the SCSS to CSS, creates new versions and updates the base.html file with the new versions.  The originals directory always has the base filename, so that it is possible to see the changes in git, just like normal.  For images, the S3 updater simply sends the file to S3.
5. Links - it is possible to create popup links to standalone paragraphs, paragraph pages that show only one standalone paragraph, reference links to the web page being referenced or even group links to a page that shows the ordered paragraphs for a given group.  These links are created programmatically using indicators such as |beg|para_slug|end| or |beg_ref|reference_slug|end_ref|.  All links are color-coded: bright blue for internal links that will take you away from the current page, maroon for pop-ups and dark blueish-gray for external links that will open a new tab.  The differences may not be distinguishable to color-blind people at this time, unless they can read which class is assigned to the link.
6. Another advantage of creating references or groups ahead of time, is that you have the slugs to create the links as part of paragraph writing process. For the same reasons, especially when writing ordered paragraphs within a group, creating paragraph stubs makes organizing thoughts easier and allows for creating links to the stubbed paragraph. If you are planning something complex with lots of links, it is easy to [write SQL](https://github.com/lizschley/number_six/blob/develop/originals/sql/create_modal_link_indicators.sql) to do this for you.
7. Reordering Paragraphs within Groups - normally creating and deleting associations is all that is needed.  But sometimes you want to reorder the paragraphs within a group. To do this, you [retrieve the data by the group id](https://github.com/lizschley/number_six/blob/develop/data/data_for_updates/dev_input_step_one/save/group_ids.json) and order the paragraphs by moving them in the order you want.  I wrote a separate [reordering script](https://github.com/lizschley/number_six/blob/develop/scripts/db_change_order.py) for that, since it is rare, but painstaking work. Read the usage instructions.

My experience was that having all of those paragraphs in front of me, made me want to update the paragraph text.  Although the change order script only updates the paragraph order, but the same input can be reused with the normal Step 3 DB Update.

## Creates and Updates in Production
I have lots of plans to automate this, but for now there are no real pain points.  Once the process is no longer new, the exact automation needed will become clear.
### Step One
Since development is the source of truth, [db_updater_s3](https://github.com/lizschley/number_six/blob/develop/scripts/db_updater_s3.py) is only run in development.  We have special input data designed for updating production: [retrieval based on updated date](https://github.com/lizschley/number_six/blob/develop/data/data_for_updates/dev_input_step_one/save/num_days_before.json).  It can be changed to hours.  Changing it to be weeks would work, but would be too long to wait.

It is important to use the for_prod parameter when retrieving data to update prodcution (see the db_updater scripts for usage) In Step One this does two things:
1. Names the input file correctly
2. Creates a lookup table that associates a given development id to the unique key for the corresponding record.  Usually these are slugs, but for paragraphs, we use a guid.  This is vital information when creating new association.
### Step Two - always skip when updating production
### Step Three
[db_updater_s3](https://github.com/lizschley/number_six/blob/develop/scripts/db_updater_s3.py) can be run in development or in production. If it is in the production environment, using the for_prod argument will raise an error.  In step three, the for_prod variable is for testing production code in a test environment.

For the production environment (and non-production with for_prod argument (testing only)):
1. Input data will be in [<PROD_INPUT_JSON>](https://github.com/lizschley/number_six/blob/develop/constants/scripts.py).
2. Class used will be ParaDbUpdateProcessProd

Some additional information about running in production:
1. ParaDbUpdateProcessProd will raise an error if there is no lookup table (see Step One above)
2. ParaDbUpdateProcessProd will raise an error if there are any add_* keys (explicit creates not allowed)
3. Data is created in production, by looking up the development record (supplied by the Step One data retrieval that was run in development) with the unique key.  If the record does not exist, it is created.
4. Once the new record is found or created, the production primary key is added to the lookup table.  When it comes time to process associations, we can create the associations using the production ids instead of the devlopment ids.
