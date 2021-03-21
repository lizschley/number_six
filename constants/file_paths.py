'''File path constants used for non-test data, besides scripts (see constants/scripts)'''
import os
from decouple import config
import portfolio.settings as settings


if config('ENVIRONMENT') == 'development':
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/reverse_resume_private.json')
else:
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/urban_coyotes.json')

S3_CLOUDFRONT = 'https://dirl4bhsg8ywj.cloudfront.net/static/'

BASE_HTML = os.path.join(settings.BASE_DIR, 'templates/base.html')
INPUT_DIR = os.path.join(settings.BASE_DIR, 'data/input')
