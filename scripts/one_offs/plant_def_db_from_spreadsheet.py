'''
    Plan to make this obsolete!!!

    Turn csv into dictionary that can be used to update database, this is a one-off
    because it is a unique csv

    Uses ParagraphDbJsonInputCreator to write the json
    May also update database directly

:return: 'ok' or error message
:rtype: str
'''
# pylint: disable=missing-function-docstring
import csv
import os
from common_classes.para_db_create_process import ParaDbCreateProcess
from common_classes.paragraph_db_input_creator import ParagraphDbInputCreator
import helpers.no_import_common_class.paragraph_helpers as no_import_helper
from portfolio.settings import BASE_DIR


IN_CSV_FILE = os.path.join(BASE_DIR, 'data/csv/botany_vocabulary.csv')
# #first_letter: 'add first letter to link (#A for ex) and link_text (_A for ex)'
# term: add term to link(/term) and link_text (just term)
VALID_ADD_TEXT = ('#first_letter', 'term')


def run(*args):
    '''
        usage as follows:
        > python manage.py runscript -v3 plant_def_db_from_spreadsheet
        or
        > python manage.py runscript -v3 plant_def_db_from_spreadsheet --script-args create_para='yes'
    '''
    print(f'csv input = {IN_CSV_FILE}')
    # will be reworking ParagraphDbInputCreator around json file processing
    json_creator = ParagraphDbInputCreator(title='Botany Definitions')
    json_creator = process_csv(json_creator)
    if create_para_directly(args):
        updating = True
        para_to_db = ParaDbCreateProcess(updating)
        para_to_db.dictionary_to_db(json_creator.output)
    else:
        json_creator.write_json_file()


def process_csv(json_creator):
    with open(IN_CSV_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            line_count += 1
            json_creator = process_row(row, json_creator, line_count)
        return json_creator


def process_row(row, json_creator, line_count):
    para_id = f'num_{line_count}'
    subtitle = row['term']
    text = row['desc']
    link_text = form_link_text(row['link_text'], row['add_text'], row['term'])
    url = form_url(row['link'], row['add_text'], row['term'])
    text = [row['desc']]
    ref = ParagraphDbInputCreator.reference_dictionary(link_text, url)
    para = ParagraphDbInputCreator.paragraph_dictionary(para_id, text, subtitle)
    ref_link_para = ParagraphDbInputCreator.ref_link_para_dictionary(para_id, link_text)
    json_creator.assign_output(ref, para, ref_link_para)
    return json_creator


def form_link_text(link_text, add_text, term):
    if add_text == '#first_letter':
        return link_text + term[0]
    if add_text == 'term':
        return link_text + term
    return link_text


def form_url(url, add_text, term):
    if add_text == '#first_letter':
        return url + '#' + term[0].upper()
    if add_text == 'term':
        return url + '/' + term
    return url


def create_para_directly(args):
    '''
    create_para_directly will check if the create_para switch is 'yes' or 'no'

    :param args: args sent in.  Currently the only one is create_para
    :type args: tuple
    :return: True or False
    :rtype: bool
    '''
    possibilities = no_import_helper.check_for_batch_args(args, 'create_para')
    if len(possibilities) != 1:
        return False
    possibility = possibilities[0]
    process_array = possibility.split('=')
    if len(process_array) != 2:
        return False
    return process_array[1] == 'yes'
