'''class for any boto3 automation '''
# pylint: disable-msg=C0103
import os
import shutil
from decouple import config
import sass
from common_classes.aws_automater import AwsAutomater
import constants.s3_data as lookup
import utilities.random_methods as utils


class StaticFiles(AwsAutomater):
    ''' Use this for all of the aws automation '''

    def __init__(self, s3_data_key, is_prod=False, is_home=False):
        '''
        __init__ start static processing

        Automation moving towards automating S3 as easily as updating a file with the results versioned
        by Github

        Usage - edit the file in the originals directory (except for images, just manually copy as many
                as you want to upload to the upload directory)

        Images will always have more manual steps, since they will usually be updated once only.  This
        will be more true once I have some standards worked out.

        :param s3_data_key: used to find information needed to process one group at a time. For example,
                            only images in home, or only the script.js
        :type s3_data_key: str
        :param is_prod: development and production are processed differently.  The filenames in
                        production will not be versioned with _9.  Defaults to False
        :type is_prod: bool, optional
        '''
        super().__init__()
        self.is_prod = is_prod
        self.is_home = is_home
        self.is_css = s3_data_key == 'css'
        self.is_an_image = s3_data_key == 'image'
        self.versions = {}
        self.file_data = lookup.S3_DATA[s3_data_key]
        self.base_html = lookup.S3_DATA['base_html']
        self.upload_dir = lookup.S3_DATA['upload_dir']
        if not self.is_an_image:
            self.original_dir = lookup.S3_DATA['originals_base'] + self.file_data['original_dir']

    def file_update_process(self):
        ''' file_update_process calls each of the steps needed to upload a file to s3
            and then to delete or achive the file from the upload directory
        '''
        if self.is_css:
            self.compile_original_to_upload()
        if self.is_an_image:
            self.loop_through_images()
            return
        files = self.adjust_versions()
        utils.copy_file_from_source_to_target(files['file_source'], files['file_target'])
        params = {
            'path_to_file': files['file_target'],
            's3_name': files['s3_key'],
            'content_type': self.file_data['content_type']
        }
        self.upload_file_to_s3(**params)
        self.delete_old_versions(files['file_target'])

    def compile_original_to_upload(self):
        ''' For scss files that are updated, need to compress file before doing anything else
            The css file will be added to the originals directory and the versioning done as normal
            with the css file, not the scss file. '''
        sass.compile(dirname=(self.file_data['scss_file'],
                              self.original_dir),
                     output_style='expanded')

    def loop_through_images(self):
        ''' Loops through images in directory and processes each individually '''
        for filename in os.listdir(self.upload_dir):
            content_type = self.image_content_type(filename)
            if not content_type:
                continue
            input_path = os.path.join(self.upload_dir, filename)
            s3_name = self.file_data['home_key'] if self.is_home else self.file_data['projects_key']
            s3_name += filename
            params = {
                'path_to_file': input_path,
                's3_name': s3_name,
                'content_type': content_type
            }
            self.upload_file_to_s3(**params)
            image_archive = config('ARCHIVE', default='')
            if len(image_archive) > 10:
                shutil.move(input_path, image_archive)

    def image_content_type(self, filename):
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

    def adjust_versions(self):
        '''
        adjust_versions is not implemented yet.
        In order to test make sure versions in update_base_url are manually set correctly
        '''
        self.update_base_html()
        return self.create_new_version()

    def update_base_html(self):
        ''' Updating the return manually for now.  Starting out with 1 since the theme has never been
            versioned
        '''
        self.versions['current'] = 10
        self.versions['prior'] = 9

    def create_new_version(self):
        '''
            If the manual versions are set correctly (in update_base_html), this should work
            Although the images are not yet implemented
        '''
        if self.is_an_image:
            return
        # variable = something if condition else something_else
        version = str(self.versions['current'])
        versioned_filename = self.use_filename(version)
        original_filename = self.file_data['base_filename'] + self.file_data['extension']
        target = self.upload_dir + '/' + versioned_filename
        source = self.original_dir + original_filename
        s3_object = self.file_data['prelim_s3_key'] + versioned_filename
        return {'file_source': source,
                'file_target': target,
                's3_key': s3_object}

    def delete_old_versions(self, path_to_uploaded_file):
        '''
            delete files in upload_to_s3
            delete old versions on s3
            if prod
                invalidate cache in cloudfront
        '''
        os.remove(path_to_uploaded_file)
        if self.is_prod:
            self.invalidate_s3_cache(f'{self.file_data["prelim_s3_key"]}*')
            return
        if self.versions['prior'] == 0:
            return
        prior_filename = self.use_filename(str(self.versions['prior']), False)
        s3_object = self.file_data['prelim_s3_key'] + prior_filename
        self.delete_file_on_s3(s3_object)

    def use_filename(self, version, is_current=True):
        '''
        use_filename creates the filename that we will use for both the s3 filename
        and for the file in the upload_to_s3 directory

        :return: filename used in multiple places
        :rtype: str
        '''
        if self.is_an_image:
            return
        base = self.file_data['base_filename']
        ext = self.file_data['extension']
        if self.is_prod and is_current:
            return base + ext
        return base + '_' + version + ext
