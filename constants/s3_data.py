''' Use these constants for S3 processing '''
import os
import constants.file_paths as file_path
import settings


S3_DATA = {
    'upload_dir': os.path.join(settings.BASE_DIR, 'upload_to_s3'),
    'base_html': file_path.BASE_HTML,
    'image': {
        'home_communities': 'static/plant_images/home_plant_communities',
        'still_native': 'static/plant_images/native_va',
        'vaguely_native': 'static/plant_images/native_east_north_america',
        'non-native': 'static/plant_images/non-native',
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
