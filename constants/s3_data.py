''' Use these constants for S3 processing '''
import os
import constants.file_paths as file_path
import portfolio.settings as settings


S3_DATA = {
    'upload_dir': os.path.join(settings.BASE_DIR, 'upload_to_s3'),
    'originals_base': os.path.join(settings.BASE_DIR, 'originals'),
    'base_html': file_path.BASE_HTML,
    'css': {
        'scss_dir': os.path.join(settings.BASE_DIR, 'originals/css/uncompiled'),
        'base_filename': 'theme',
        'prelim_s3_key': 'static/css/',
        'extension': '.css',
        'original_dir': '/css/',
        'content_type': 'text/css',
    },
    'cat': {
        'base_filename': 'categories',
        'prelim_s3_key': 'static/js/',
        'extension': '.js',
        'original_dir': '/js/',
        'content_type': 'text/javascript',
    },
    'flashcard': {
        'base_filename': 'flashcard',
        'prelim_s3_key': 'static/js/',
        'extension': '.js',
        'original_dir': '/js/',
        'content_type': 'text/javascript',
    },
    'script': {
        'base_filename': 'script',
        'prelim_s3_key': 'static/js/',
        'extension': '.js',
        'original_dir': '/js/',
        'content_type': 'text/javascript',
    },
    'image': {
        'home_key': 'static/home/img/',
        'projects_key': 'static/projects/img/',
    },
}
