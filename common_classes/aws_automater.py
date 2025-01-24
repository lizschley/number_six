''' class for any boto3 automation '''
# pylint: disable-msg=C0103
import os
import sys
import boto3
import settings

current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

# now we can import the module in the parent
# directory.


class AwsAutomater:
    ''' Use for all aws automation '''

    def __init__(self):
        ''' Establish credentials, region and reusable S3 information '''
        self.session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.s3 = self.session.resource('s3')
        self.bucket_name = settings.AWS_S3_BUCKET_NAME

    def test_credentials(self):
        ''' testing 
            arn:aws:s3:::lizschley-static/*
            arn:aws:s3:::lizschley-static        
        '''
        test_bucket = self.s3.Bucket(self.bucket_name)

        for s3_file in test_bucket.objects.all():
            print(s3_file.key)

    def upload_file_to_s3(self, **kwargs):
        '''
        upload_file_to_s3 uploads a file to s3

        kwargs = {
            'path_to_file': passed in file_path
            's3_name': s3_object_name
            'content_type': content_type
        }
        '''
        print(f'Uploading file to S3: {kwargs}')
        new_obj = self.s3.Object(self.bucket_name, kwargs['s3_name'])
        new_obj.upload_file(kwargs['path_to_file'], ExtraArgs={'ContentType': kwargs['content_type']})

    # delete is not available
    def delete_file_on_s3(self, key):
        ''' Delete object with passed in key '''
        print(f'Deleting {key} from s3 bucket: {self.bucket_name}')
        self.s3.Object(bucket_name=self.bucket_name, key=key).delete()

    @staticmethod
    def upload_params(path_to_file, s3_name, content_type):
        '''
        upload_params used for uploading files to S3

        :return: params to upload S3
        :rtype: dictionary
        '''
        return {
            'path_to_file': path_to_file,
            's3_name': s3_name,
            'content_type': content_type
        }
