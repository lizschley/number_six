import os
import sys
import settings
from common_classes.aws_automater import AwsAutomater
import constants.s3_data as lookup


class ImageUpload(AwsAutomater):
    ''' Use this for all of the aws automation '''

    def __init__(self):
        '''
        __init__ start static processing

        Goal - make it so static files are as easy to update as if they were stored in file system with
               no caching worries.  Using github (css & js) or google (images), not S3 for versioning

        Usage - For js or scss, edit the file in the originals directory.  For images, just manually
                copy as many images as you want to upload to the upload directory (note - do home images
                separately from projects image.  Not versioning images.)

        Called from scripts/s3_updater.py (see script documentation)
        '''
        print(f"Basedir: {settings.BASE_DIR}")
        super().__init__()

    def image_uploader(self):
        self.assign_variables()
        self.loop_through_directories()

    def assign_variables(self):
        '''
            assign_variables based on what is passed in.  There should be only one s3 data key at a time
            # These are the kwargs needed for  
            kwargs = {
                'path_to_file': passed in file_path
                's3_name': s3_object_name
                'content_type': content_type
            }
        '''
        self.file_data = lookup.S3_DATA['image']
        self.file_data['upload_dir'] = lookup.S3_DATA['upload_dir']

    def loop_through_directories(self):
        ''' Loops through directories to process file directory and files individually '''
        for dir_name in os.listdir(self.file_data['upload_dir']):
            dir_path = os.path.join(self.file_data['upload_dir'], dir_name)
            # checking if it is a file
            if '.DS_Store' in dir_path:
                continue
            elif os.path.isfile(dir_path):
                sys.exit(f'Error!  Expecting only directories, but got: {dir_path}')
            self.loop_through_files(dir_path, dir_name)

    def loop_through_files(self, dir_path, dir_name):
        ''' Loops through images in directory and processes each individually '''
        for filename in os.listdir(dir_path):
            content_type = self.image_content_type(filename)
            if not content_type:
                continue
            file_path = os.path.join(dir_path, filename)
            if os.path.isdir(file_path):
                sys.exit(f'Error!  Expecting only files, but got: {file_path}')

            # this will become content_type when we are dealing with actual images
            params = self.upload_params(file_path,
                                        f'{lookup.S3_DATA['image'][dir_name]}/{filename}',
                                        content_type)
            print(f"AWS Params: {params}")
            self.upload_file_to_s3(**params)
 
    @staticmethod
    def image_content_type(filename):
        '''
        image_content_type based on the file extension

        :param filename: image file to upload
        :type filename: str
        :return: content type
        :rtype: str
        '''
        if filename.endswith('.jpg'):
            return 'image/jpeg'
        if filename.endswith('.png'):
            return 'image/png'
        return None
