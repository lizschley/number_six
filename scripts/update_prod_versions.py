'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Update data/file_data/static_file_versions.json as part of the development to master merge process
'''
import sys
import constants.scripts as constants


def run():
    '''
        Usage:
        >>> python manage.py runscript -v3 update_prod_versions
    '''
    update_versions_json()


def update_versions_json():
    ''' Copies development versions to prod versions '''

