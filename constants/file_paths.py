'''File path constants, not terribly useful reight now'''
import os
import settings

INPUT_DIR = os.path.join(settings.BASE_DIR, 'data/input')

IMAGE_PATHS = {
    'community': {}, 'east_us': {}, 'virginia': {}, 'non_native': {},
}

JSON_EXT = 'json'
