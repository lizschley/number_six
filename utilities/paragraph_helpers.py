import json
from common_classes.paragraphs_for_display import ParagraphsForDisplay


def create_link(url, link_text):
    return f'<a href="{url}" target="_blank">{link_text}</a>'


def json_to_dict(json_path):
    # Opening JSON file
    f = open(json_path, 'r')
    # load and return JSON object as a dictionary
    data = json.load(f)
    f.close()
    return data


def paragraph_list_from_json(json_path):
    dict_data = json_to_dict(json_path)
    paragraphs = ParagraphsForDisplay()
    return paragraphs.dict_to_paragraph_list(dict_data)


def format_json_text(text):
    text = ' '.join(text)
    if text[0] != '<':
        text = '<p>' + text + '</p>'
    return text





