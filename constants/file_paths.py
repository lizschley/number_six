'''File path constants used for non-test data.'''

import os
import portfolio.settings as settings
from decouple import config


if config('ENVIRONMENT') == 'development':
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/reverse_resume_private.json')
else:
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/urban_coyotes.json')


S3_CLOUDFRONT = 'https://dirl4bhsg8ywj.cloudfront.net/static/'
COMPILE_SCSS = os.path.join(settings.BASE_DIR, 'originals/compile')
UPLOAD_TO_S3 = os.path.join(settings.BASE_DIR, 'uploads/css')
