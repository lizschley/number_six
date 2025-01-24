''' Use these constants for S3 processing '''
import os
import settings


S3_DATA = {
    'archive_dir': os.path.join(settings.HOME, 'Document', 'web_images'),
    'upload_dir': os.path.join(settings.BASE_DIR, 'upload_to_s3'),
    'image': {
        'community': 'basic_website/home_plant_images/communities',
        'virginia': 'basic_website/home_plant_images/native_va',
        'east_us': 'basic_website/home_plant_images/native_east_us',
        'non_native': 'basic_website/home_plant_images/non_native',
        # the keys and paths below are no longer used by an application
        'home_key': 'static/home/img/',
        'projects_key': 'static/projects/img/',
    },
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
}
