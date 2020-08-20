'''File path constants used for non-test data.'''

import os
import portfolio.settings as settings

if os.getenv('ENVIRONMENT') == 'production':
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/urban_coyotes.json')
else:
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/reverse_resume_private.json')
