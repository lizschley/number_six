'''File path constants used for non-test data, besides scripts (see constants/scripts)'''
import os
import settings

S3_CLOUDFRONT = 'https://dirl4bhsg8ywj.cloudfront.net/static/'

BASE_HTML = os.path.join(settings.BASE_DIR, 'templates/base.html')
INPUT_DIR = os.path.join(settings.BASE_DIR, 'data/input')
