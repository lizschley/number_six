import json


def create_link(url, link_text):
    return f'<a href="{url}" target="_blank">{link_text}</a>'


def json_to_dict(json_path):
    # Opening JSON file
    f = open(json_path, 'r')
    # load and return JSON object as a dictionary
    data = json.load(f)
    f.close()
    return data


def format_json_text(text):
    text = ' '.join(text)
    if text[0] != '<':
        text = '<p>' + text + '</p>'
    return text


def ensure_unique_slug(sender, instance, slug):
    new_slug = slug
    while True:
        if not_unique(sender, new_slug):
            new_slug = f'{slug}-{instance.id}'
        else:
            break
    return new_slug


def not_unique(sender, slug):
    return sender.objects.filter(slug=slug).exists()


def extract_data_from_form(classification):
    temp = classification.split('_')
    if len(temp) != 2:
        return {}
    try:
        return {temp[0]: int(temp[1])}
    except ValueError:
        return {}
