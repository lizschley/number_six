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
        super().__init__(after_load=lookup.S3_DATA['after_load'])

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
        self.file_data['archive_dir'] = lookup.S3_DATA['archive_dir']

    def loop_through_directories(self):
        ''' Loops through directories to process file directory and files individually '''
        for dir_name in os.listdir(self.file_data['upload_dir']):
            # todo - need both in_dir_path and out_dir_path here (rest will be the same)
            in_dirpath = os.path.join(self.file_data['upload_dir'], dir_name)
            out_dirpath = os.path.join(self.file_data['archive_dir'], dir_name)
            if '.DS_Store' in in_dirpath:
                continue
            elif os.path.isfile(in_dirpath):
                sys.exit(f'Error!  Expecting only directories, but got: {in_dirpath}')
            self.loop_through_files(in_dirpath, out_dirpath, dir_name)

    def loop_through_files(self, in_dirpath, out_dirpath, dir_name):
        ''' Loops through images in directory and processes each individually '''
        for filename in os.listdir(in_dirpath):
            content_type = self.image_content_type(filename)
            if not content_type:
                continue

            # this can be a random method called twice
            in_filepath = os.path.join(in_dirpath, filename)
            out_filepath = os.path.join(out_dirpath, filename)
            if os.path.isdir(in_filepath):
                sys.exit(f'Error!  Expecting only files, but got: {in_filepath}')

            params = self.upload_params(in_filepath,
                                        out_filepath,
                                        f'{lookup.S3_DATA['image'][dir_name]}/{filename}',
                                        content_type)
            print(f"AWS Params: {params}")
            self.upload_file_to_s3(**params)

    def list_s3_objects(self, bucket_name=settings.AWS_S3_BUCKET_NAME, prefix='basic_website/travel/hawaii'):
        try:
            objects = []
            kwargs = {'Bucket': bucket_name, 'Prefix': prefix}

            while True:
                response = self.s3_client.list_objects_v2(**kwargs)
                if 'Contents' in response:
                    objects.extend([obj['Key'] for obj in response['Contents']])
                try:
                    kwargs['ContinuationToken'] = response['NextContinuationToken']
                except KeyError:
                    break
        except Exception as e:
            print(f"Error listing objects: {str(e)}")
        for obj in objects:
            print(f'success! {obj}')

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
