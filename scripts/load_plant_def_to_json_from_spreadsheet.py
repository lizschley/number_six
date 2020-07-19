# pylint: disable=missing-function-docstring

'''
    [summary]

[extended_summary]

:return: [description]
:rtype: [type]
'''
import os
import csv
import json
from portfolio.settings import BASE_DIR

IN_CSV_FILE = os.path.join(BASE_DIR, 'data/csv/plant_vocabulary.csv')
OUT_JSON_FILE = os.path.join(BASE_DIR, 'data/plant_vocabulary.json')
ADD_TEXT = {
    '#first_letter': 'add first letter to link (#A for ex) and link_text (_A for ex)',
    'term': 'add term to link(/term) and link_text (just term)'

}


def run():
    '''
        usage as follows:
        > python manage.py runscript -v3 load_plant_def_to_json_from_spreadsheet
    '''
    print(f'base dir = {BASE_DIR}')
    print(f'csv input = {IN_CSV_FILE}')
    out_dictionary = starting_dictionary()
    print(f'out_dictionary == {out_dictionary}')
    print(f'out_dictionary is a {type(out_dictionary)}')

    in_csv_dictionary = starting_csv()
    print(f'in_csv_dictionary == {in_csv_dictionary}')
    print(f'in_csv_dictionary is a {type(in_csv_dictionary)}')


def starting_csv():
    with open(IN_CSV_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            # else:
            #     print(f'for line #{line_count}')
            #     print(f'term == {row["term"]}')
            #     print(f'definition == {row["desc"]}')
            #     print(f'link == {row["link"]}')
            #     print(f'link_text == {row["link_text"]}')
            #     print(f'add_text == {row["add_text"]}')
        return csv_reader


def starting_dictionary():
    return {
        "group": {
            "title": "Botany Definitions",
            "note": "",
            "ordered": "no",
            "standalone": "yes"
        },
        "references": [
            {
                "link_text": "",
                "url": ""
            }
        ],
        "paragraphs": [
            {
                "id": "",
                "subtitle": "",
                "note": "",
                "text": [
                ]
            }
        ],
        "ref_link_paragraph": [
            {
                "link_text": "",
                "paragraph_id": ""
            }
        ]
    }
