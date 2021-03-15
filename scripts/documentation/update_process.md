# Create and Update Development and Production Data
## Development vs Production
For this portfolio application, the development data is the source of truth.  If the production site came down, the site will still be available in its entirety in development.  Any updates in production, should result it identical data to development: in text, records and associations between records.  For that reason, the development and production update processes are quite different.

The goal is the same.  Creates, retrievals, updates and deletions (besides research and writing) should be easy.
## Record Types
1. Paragraphs - the main unit for the text that is displayed dynamically on the site
2. Groups - describe to the application how the paragraphs are displayed
3. References - show where the information comes from.  One exception, if the reference is not online, the information will be directly associated with the paragraph using the text field
4. GroupParagraph - associates a paragraph with a Group.  This is a many-to-many relationship.  Sometime paragraphs are ordered within a given group.  For that reason, there is order field in the GroupParagraph record.
5. ParagraphReference - associates a paragraph with a reference.  It is also a many-to-many relationship
6. Category - associates one category with many groups.  Groups can be ordered using the cat_sort field in the group record.
## Creating Paragraph Data
The normal create process runs only in development.  It will throw an error if you try to run it in production.  The script is scripts/create_paragraphs.py and corresponds to a class (ParaDbCreateProcess). The input data is in json format and uses this template: data/update_and_create_json_templates/create_dev_input_template.json.  Using this template, you can create a group with multiple associated paragraphs.  You can also create many references.

The paragraph creation is for one group at a time and there is no way to create a paragraph without a group. Each paragraph within a "paragraphs" list will be automatically associated with the group.  If the group already exists, the create process uses the group["group_title"] to look up the group record and automatically associates the paragraph with the group.  If the group is found, the program will ignore any other group fields.  Sometimes paragraphs within a group are ordered.  This will happen programmatically, based on the paragraph order in the input data's paragraphs list.

Reference / paragraph associations are automatically set up using a "link_text_list": [] within each paragraph associated with the given reference.  If one reference is associated with multiple paragraphs, the reference's link_text field must be in the link_text_lists for multiple paragraphs.
## Development Update
Paragraphs are treated differently in the development process, because of their complexity. They contain most of the text and all of the html formatting, paths to images, css classes used to display those images and information to create various kinds of links during the paragraph display process.  The only way to create new paragraphs is by using ParaDbCreateProcess (see above).

The update process uses the script/db_updater scripts, which contain usage information, and the ParaDbUpdate classes.

You can create the following records using the db_update process: category, group, reference, group_paragraph and paragraph_reference
You can update the following records using the db_update process: paragraph, category, group, reference and group_paragraph
You can delete the following records using the db_update process: group_paragraph and paragraph_reference
### Step One
To update records, it is important to retrieve the existing record.  This is what step one does.  It also retrieves all the related data.  To retrieve only the data you want to update, send in information, such as record ids.  All of the possibilites for retrieving the records and their related data are in data/update_and_create_json_templates/update_dev_input_template.json. The script will loop through the json files in the data/data_for_updates directory.

Generally, I move a file in the /data/data_for_updates/dev_input_step_one/save folder to the dev_input_step_one directory and modify it to be what I want.

Step One is only for data retrievals.  To add new data, for example groups or categories, you can by-pass this step entirely.  It can be useful, however, to retrieve unique keys.  For example, if you want to create a new association, it helps to retrieve the slug or paragraph guid needed for the input data.
### Step Two
Step One writes the data it retrieves to the data/data_for_updates/dev_input_step_three directory.  Step 2 is the manual editing phase.  It is possible, but not necessary to delete data that does not need to be updated.
### Step Three
Once the data is modified, run scripts/db_updater_s3.py.  It will loop through any files and make the database updates.

It uses the json keys to find the data and process it in order:
1. 'add_categories'
2. 'add_groups'
3. 'add_references'

Then it does updates using the following keys in order:
1. 'categories'
2. 'references'
3. 'paragraphs'
4. 'groups'
5. 'paragraph_reference'
6. 'group_paragraph'

The order is important, because groups have a category_id which depends on the category already being created.  Association records need both the parent records to have already been created.

If there is an error, processing stops.  The process is not entirely idempotent, because paragraphs can be duplicated.  Mistakes are easy to recover from and due to carelessness.
### In Practice
1. Explicit Creates - Groups can be created as part of the planning process. It is often easier to create groups and references ahead of time using the the updater, as opposed to during the create process.  It varies with the complexity and planned format of the data being created.
2. Update single records - often, all of the other records are set, but the wording is not right.  For that reason, you can get just paragraphs by sending in paragraphs=4,5,6 for example, where 4, 5 & 6 are paragraph ids.  This brings only the paragraphs. You can do this for groups or categories as well, in case you have an orphan group you would like to edit, for example.  The directions for this is in the scripts/db_updater_s3.py.  I have sql to get the ids, see originals/sql/list_of_comma-delimited_ids.sql, that I alter to get the data I want.
3. Create in html - html tags are stored in the paragraph records.  Often I type this directly in the json file.  But for complex html coding, it is helpful to use helpers/tag_finisher.html so that vscode will complete the tags and the html and be tested ahead of time.
4. Static Files - all the static files (css, js and images) are on S3.  The css and js are versioned, so that caching is not an issue. To make this process more convenient, there is a script called scripts/s3_updater.py that compiles the SCSS to CSS, creates new versions and updates the base.html file with the new versions.  The originals directory always has the base filename, so that it is possible to see the changes in git, just like normal.  For images, the S3 updater simply sends the file to S3.
5. Links - it is possible to create popup links to standalone paragraphs, paragraph pages that show only one standalone paragraph, reference links to the web page being refenced or even group links to a page that shows the ordered paragraphs for a given group.  These links are created programmatically using indicators such as |beg|para_slug|end| or |beg_ref|reference_slug|end_ref|.  All links are color-coded: bright blue for internal links off the page, maroon for pop-ups and dark blueish-gray for external links.  These links are not accessible to color-blind people at this time.
6. Another advantage of creating references or groups ahead of time, is that you have the slugs to create the links as part of writing the paragraph. For the same reasons, especially when writing ordered paragraphs within a group, creating paragraph stubs makes organizing thoughts easier and allows for creating links to the stubbed paragraph. If there are a lot of links, it is easy to write SQL to do this for you. originals/sql/create_modal_link_indicators.sql
7. Reordering Paragraphs within Groups - normally creating and deleting associations is all that is needed.  But sometimes you want to reorder the paragraphs within a group. I wrote a separate script for that, since it is rare. You can retrieve the data by the group id and order the paragraphs by moving them in the order you want.  The program does not update the text, but if you make some changes, you can run db_updater_s3 with the same input data.

## Production Create and Update
I have lots of plans to automate this, but for now there are no real pain points.  Once the process is no longer new, the exact automation needed will become clear.
### Step One
Since development is the source of truth, scripts/db_updater_s1 is always run in development.  We have special input data designed for updating production: data/data_for_updates/dev_input_step_one/save/num_days_before.json.  It can be changed to hours or weeks (not recommended), as well.

It is important to use the for_prod parameter (see the script for usage) in Step 1.  This does two things:
1. Names the input file correctly
2. Creates a lookup table that associates a given development id to the unique key for the corresponding record.  Usually these are slugs, but for paragraphs, we use a guid.  This is vital information when creating new association.
### Step Two - always skip when updating production
### Step Three
scripts/db_updater_s3 can be run in development or in production. If it is in the production environment, using the for_prod argument will raise an error.  In step three, the for_prod variable is for testing code meant for production in a different environment.

For the production environment (and non-production with for_prod argument (testing only)):
1. Input data will be data/data_for_updates/prod_input_json.
2. Class used will be ParaDbUpdateProcessProd

Some additional information about running in production:
1. ParaDbUpdateProcessProd will raise an error if there is no lookup table (see step One above)
2. ParaDbUpdateProcessProd will raise an error if there are any add_* keys (explicit creates not allowed)
3. Data is created in production, by looking up the development record (supplied by the Step One data retrieval that was run in development) with the unique key.  If the record does not exist, it is created.
4. Once the new record is found or created, the production primary key is added to the lookup table.  When it comes time to process associations, we can create the associations using the production ids instead of the devlopment ids.
