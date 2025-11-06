''' methods for accordion functionality '''
import textwrap

TWENTY_SPACES = '                      '
SIXTEEN_SPACES = '                '


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


def make_carousel_indicator_lines(vars):
    # need nums and carousel_id
    lines = ''
    for idx in range(len(vars['urls'])):
        num = idx + 1
        lines += SIXTEEN_SPACES + f'<button type="button" data-bs-target="#{vars['carousel_id']}" data-bs-slide-to="{num}" class="active" aria-current="true" aria-label="Image {num}"></button>\n'
    return lines


def make_carousel_item_divs(vars):
    # need urls and alt_text
    urls = vars['urls']
    lines = f'{SIXTEEN_SPACES}<div class="carousel-item active"> \n'
    idx = 0
    for idx in range(len(urls)):
        alt_text = alt_text_from_url(urls[idx])
        if idx > 0:
            lines += f'{SIXTEEN_SPACES}<div class="carousel-item">\n'
        lines += f'{TWENTY_SPACES}<img src="{urls[idx]}" class="d-block w-100" alt="{alt_text}">\n'
        lines += f'{SIXTEEN_SPACES}</div>' + '\n'
        idx += 1
    return lines


def alt_text_from_url(url):
    temp = url.split('/')
    fn = temp.pop()
    temp = fn.split('.')
    return f'image called {temp[0]}'






