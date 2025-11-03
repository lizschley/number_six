''' class for any boto3 automation '''
# pylint: disable-msg=C0103
import os
import sys
import boto3
import settings
import pprint
from botocore.exceptions import ClientError
from utilities import file_utils as utils

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
        ''' Establish credentials '''

        sts = boto3.client(
                        'sts',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                    )

        # Request temporary credentials
        response = sts.get_session_token(DurationSeconds=3600)

        # Display the temporary credentials
        # print(response)

        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=response['Credentials']['AccessKeyId'],
                                      aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                      aws_session_token=response['Credentials']['SessionToken'])
        self.bucket_name = settings.AWS_S3_BUCKET_NAME

    def test_credentials(self):
        ''' testing
            arn:aws:s3:::lizschley-static/*
            arn:aws:s3:::lizschley-static
        '''
        paginator = self.s3_client.get_paginator('list_objects')
        result = paginator.paginate(Bucket=self.bucket_name, Delimiter='/')
        for prefix in result.search('CommonPrefixes'):
            print(prefix.get('Prefix'))

    # need to pass in key word arguments for output_path and also use existing info for output_path
    # probably already have input path
    # use image_upload for making sure we are ready for archiving file after successful upload
    # key is kwargs['s3_name']
    def upload_file_to_s3(self, **kwargs):
        '''
        upload_file_to_s3 uploads a file to s3

        kwargs = {
            'in_filepath': in_filepath,
            'out_filepath': out_filepath,
            's3_name': s3_name,
            'content_type': content_type
        }
        '''
        print(f'Uploading file to S3: {kwargs}')
        self.s3_client.upload_file(kwargs['in_filepath'], self.bucket_name, kwargs['s3_name'],
                                   ExtraArgs={'ContentType': kwargs['content_type']})
        self.archive(kwargs['s3_name'], kwargs['in_filepath'], kwargs['out_filepath'])

    def archive(self, key, input_path, output_path):
        print(f'input path == {input_path}')
        print(f'begin output path == {output_path}')
        if self.check_s3(key):
            utils.move_file(input_path, output_path)
        else:
            print(f'Error!  Check S3 for {key}')

    def check_s3(self, key):
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            pprint.pp(response)
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True

    # delete is not available
    def delete_file_on_s3(self, key):
        ''' Delete object with passed in key '''
        print(f'Deleting {key} from s3 bucket: {self.bucket_name}')
        self.s3_client.Object(bucket_name=self.bucket_name, key=key).delete()

    @staticmethod
    def upload_params(in_filepath, out_filepath, s3_name, content_type):
        '''
        upload_params used for uploading files to S3

        :return: params to upload S3
        :rtype: dictionary
        '''
        return {
            'in_filepath': in_filepath,
            'out_filepath': out_filepath,
            's3_name': s3_name,
            'content_type': content_type
        }
