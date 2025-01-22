'''File path constants'''
import os
import settings

S3_CLOUDFRONT = 'https://dirl4bhsg8ywj.cloudfront.net/static/'

INPUT_DIR = os.path.join(settings.BASE_DIR, 'data/input')

IMAGE_PATHS = {
    'community': {}, 'east_us': {}, 'virginia': {}, 'non_native': {},

}
