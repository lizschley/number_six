''' Use these constants for S3 processing '''
import os
import constants.file_paths as file_path
import constants.s3_data as s3
import portfolio.settings as settings


BASE_FILE_DATA = {
    'base_html_path': file_path.BASE_HTML,
    'new_base_html': os.path.join(settings.BASE_DIR, 'templates/new_base.html'),
    'css': {
        'id': 'theme_css',
        'base_filename': s3.S3_DATA['css']['base_filename'],
        'extension': s3.S3_DATA['css']['extension'],
        'tag': 'link',
        'attribute': 'href'
    },
    'cat': {
        'id': 'cat_js',
        'base_filename': s3.S3_DATA['cat']['base_filename'],
        'extension': s3.S3_DATA['cat']['extension'],
        'tag': 'script',
        'attribute': 'src'
    },
    'flashcard': {
        'id': 'flashcard_js',
        'base_filename': s3.S3_DATA['flashcard']['base_filename'],
        'extension': s3.S3_DATA['flashcard']['extension'],
        'tag': 'script',
        'attribute': 'src'
    },
    'script': {
        'id': 'script_js',
        'base_filename': s3.S3_DATA['script']['base_filename'],
        'extension': s3.S3_DATA['script']['extension'],
        'tag': 'script',
        'attribute': 'src'
    }
}
