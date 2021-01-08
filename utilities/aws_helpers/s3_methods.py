''' These are methods to use when updating S3 '''
import sass
import constants.file_paths as file_paths


# Todo: this should be automated or at least put in a script
def compile_original_to_upload(**kwargs):
    '''
    compile_original_to_upload will eventually upload files that are changed to s3
    Currently it just translates scss to css and compresses the file

    Plan is to automated it and also, once production is up and running, I need to have a folder in
    S3 so I can load broken css and js without affecting someone accessing the site
    '''
    sass.compile(dirname=(file_paths.COMPILE_SCSS, file_paths.UPLOAD_TO_S3), output_style='expanded')
