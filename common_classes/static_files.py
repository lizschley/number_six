'''class for any boto3 automation '''
# pylint: disable-msg=C0103
import os
import shutil
import sys
from decouple import config
import sass
from common_classes.aws_automater import AwsAutomater
from common_classes.html_file_processer import HtmlFileProcesser
import constants.s3_data as lookup
import helpers.no_import_common_class.utilities as helper
import utilities.random_methods as utils
import utilities.date_time as dt


class StaticFiles(AwsAutomater):
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
        super().__init__()
        self.is_home = False
        self.is_css = False
        self.is_image = False
        self.versions = {}
        self.file_data = {}

    def file_upload_process(self, **kwargs):
        ''' file_upload_process calls each of the steps needed to upload a file to s3
            and then deletes or achives the file from the upload directory
            Someday it will also delete old versions from S3, but that is once
            I have automation that works every time
        '''

        self.assign_variables(**kwargs)

        if self.is_css:
            self.compile_original_to_upload()

        self.adjust_versions()

        if self.is_image:
            self.loop_through_images()
            return
        utils.copy_file_from_source_to_target(self.versions['original_filepath'],
                                              self.versions['upload_filepath'])

        params = self.upload_params(self.versions['upload_filepath'],
                                    self.versions['s3_object'],
                                    self.file_data['content_type'])
        self.upload_file_to_s3(**params)
        self.delete_old_versions()

    def assign_variables(self, **kwargs):
        '''
           assign_variables based on what is passed in.  There should be only one s3 data key at a time
        '''
        self.file_data = lookup.S3_DATA[kwargs['s3_data_key']]
        self.file_data['base_html'] = lookup.S3_DATA['base_html']
        self.file_data['upload_dir'] = lookup.S3_DATA['upload_dir']
        self.file_data['s3_data_key'] = kwargs['s3_data_key']
        if kwargs['s3_data_key'] == 'image':
            self.assign_image(kwargs['is_home'])
            return
        if kwargs['s3_data_key'] == 'css':
            self.is_css = True
        self.file_data['orig_dir'] = lookup.S3_DATA['originals_base'] + self.file_data['original_dir']

    def assign_image(self, is_home):
        '''
        assign_image does image_only assignments

        :param is_home: is_home option:  Two categories of images: home or projects
                        Script defaults to projects, because once the home page, icon and main menu
                        are completed (is_home==True), all images tags will be created programmatically
                        using the image fields in paragraph records in the database
        :type is_home: bool
        '''
        self.is_image = True
        self.is_home = is_home

    def compile_original_to_upload(self):
        ''' For scss files that are updated, need to compress file before doing anything else
            The css file will be added to the originals directory and the versioning done as normal
            with the css file, not the scss file. '''
        sass.compile(dirname=(self.file_data['scss_dir'],
                              self.file_data['orig_dir']),
                     output_style='expanded')

    def loop_through_images(self):
        ''' Loops through images in directory and processes each individually '''
        for filename in os.listdir(self.file_data['upload_dir']):
            content_type = self.image_content_type(filename)
            if not content_type:
                continue
            input_path = os.path.join(self.file_data['upload_dir'], filename)
            s3_name = self.file_data['home_key'] if self.is_home else self.file_data['projects_key']
            s3_name += filename
            params = self.upload_params(input_path, s3_name, content_type)
            self.upload_file_to_s3(**params)
            image_archive = config('ARCHIVE', default='')
            if len(image_archive) > 10:
                shutil.move(input_path, image_archive)

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

    def adjust_versions(self):
        '''
        adjust_versions is not implemented yet.
        In order to test make sure versions in update_base_url are manually set correctly
        '''
        self.create_new_versions()
        self.update_base_html()

    def update_base_html(self):
        ''' Updating the return manually for now.  Starting out with 1 since the theme has never been
            versioned
        '''
        # Todo: assign this when automation makes it safe (don't want to delete prod versions)
        file_updater = HtmlFileProcesser(self.file_data['s3_data_key'])
        base_html_ret = file_updater.update_base_html_s3_versions(self.versions['curr_version'])
        if helper.key_in_dictionary(base_html_ret, 'error'):
            sys.exit(base_html_ret['error'])
        self.versions['prior_version'] = base_html_ret['prior_version']

    def create_new_versions(self):
        '''
            If the manual versions are set correctly (in update_base_html), this should work
            Although the images are not yet implemented
        '''
        if self.is_image:
            return
        self.versions['curr_version'] = str(dt.get_current_epoch_date())
        versioned_filename = self.use_filename()
        self.versions['upload_filepath'] = self.file_data['upload_dir'] + '/' + versioned_filename
        self.versions['original_filepath'] = self.file_data['orig_dir'] + self.use_filename(True)
        self.versions['s3_object'] = self.file_data['prelim_s3_key'] + versioned_filename

    # Todo: once we have trusted automation around prod versions we can test and implement this
    def delete_old_versions(self):
        ''' This worked before, but change in versioning changes everything. Deleted prelim code.'''
        s2_obj_to_delete = self.file_data['prelim_s3_key'] + self.use_filename(False, 'prior_version')
        print(f's3 file to delete is {s2_obj_to_delete}')
        # self.delete_file_on_s3(s3_object)

    def use_filename(self, is_original=False, which='curr_version'):
        '''
        use_filename creates the filename that we will use for both the s3 filename
        and for the file in the upload_to_s3 directory

        :return: filename used in multiple places
        :rtype: str
        '''
        if self.is_image:
            return None
        base = self.file_data['base_filename']
        ext = self.file_data['extension']
        if is_original:
            return base + ext
        return base + '_' + self.versions[which] + ext
