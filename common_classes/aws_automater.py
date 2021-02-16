'''class for any boto3 automation '''
# pylint: disable-msg=C0103
import boto3
from decouple import config
import portfolio.settings as settings


class AwsAutomater:
    ''' Use for all aws automation '''

    def __init__(self):
        ''' Get items to be reused frequently '''
        self.session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.s3 = self.session.resource('s3')
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.region = settings.AWS_S3_REGION_NAME
        self.distribution_id = config('CLOUDFRONT_DISTRIBUTION_ID')

    def test_credentials(self):
        ''' just for testing '''
        for bucket in self.s3.buckets.all():
            print(bucket.name)

    def upload_file_to_s3(self, **kwargs):
        '''
        upload_file_to_s3 uploads a file to s3

        kwargs = {
            'path_to_file': passed in file_path
            's3_name': s3_object_name
            'content_type': content_type
        }
        '''
        print(kwargs)
        new_obj = self.s3.Object(self.bucket_name, kwargs['s3_name'])
        new_obj.upload_file(kwargs['path_to_file'], ExtraArgs={'ContentType': kwargs['content_type']})

        # self.s3.Object(self.bucket_name, kwargs['s3_name']).upload_file(kwargs['path_to_file'])

    def delete_file_on_s3(self, key):
        ''' dummy method for deleting.  Only one bucket name, so it's self '''
        # this only deletes versioned files
        print(f'before deletion, key to be deleted is {key}')
        if '_' not in key:
            return
        self.s3.Object(bucket_name=self.bucket_name, key=key).delete()
        print(f'deleted {key} from s3 bucket: {self.bucket_name}')

    def invalidate_s3_cache(self, s3_path):
        ''' dummy method for invalidating
            invalidate_s3_cache will invalidate the cache for the given object or wildcard
            https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html#invalidation-specifying-objects
        '''
        print(f'invaldiating s3 for {s3_path} using cloudfront distribution id: {self.distribution_id}')
