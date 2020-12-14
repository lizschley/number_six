'''File path constants used for non-test data.'''

import os
import portfolio.settings as settings

if os.getenv('ENVIRONMENT') == 'development':
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/reverse_resume_private.json')
else:
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/urban_coyotes.json')
