''' methods for accordion functionality '''
import textwrap

TWENTY_SPACES = '                      '


def create_accordion_item(**kwargs):
    parent_id = kwargs.get('parent_id', 'make_it_specific')
    target_base = kwargs.get('target_base', 'collapse')
    item_id = target_base + str(kwargs.get('index', 0))
    button_text = kwargs.get('button_text', 'no button text')
    body_lines = kwargs.get('body_lines', [])
    body_text = make_lines_text(body_lines)

    return textwrap.dedent(f'''\
        <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#{item_id}" aria-expanded="false" aria-controls="{item_id}">
                    {TWENTY_SPACES}{button_text}
                </button>
            </h2>
            <div id="{item_id}" class="accordion-collapse collapse" data-bs-parent="#{parent_id}">
                <div class="accordion-body">
                    {body_text}
                </div>
            </div>
        </div>
''')


def make_lines_text(lines):
    text = ''
    for line in lines:
        if '<p>' in line:
            text = text + TWENTY_SPACES + line + '\n'
        else:
            text = text + TWENTY_SPACES + '<p>' + line + '\n'
    return text
