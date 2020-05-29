import os
import portfolio.settings as ps

SCRIPT_PARAM_SUBSTR = {'filename': '.json', 'test_run': 'test_run:', }
JSON_KEYS_FOR_PARAGRAPHS = ('group', 'group_id', 'references', 'ref_link_paragraph', 'paragraphs')
DEMO_PARAGRAPH_JSON = os.path.join(ps.JSON_DATA_ROOT, 'demo/urban_coyotes.json')
RANDOM_SLUG_APPEND = 5
