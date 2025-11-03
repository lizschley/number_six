'''
    Update S3 using the StaticFiles class which inherites from AwsAutomater

    Goal: upload images. No longer updating other static files, but some remnents may remain.

    Note - images are not versioned.

    Run -> python scripts/s3_updater.py
'''
from common_classes.image_upload import ImageUpload


def images_to_s3():
    importer = ImageUpload()
    importer.image_uploader()


def test_access():
    importer = ImageUpload()
    importer.test_credentials()


def list_objects():
    importer = ImageUpload()
    importer.list_s3_objects()


if __name__ == '__main__':
    # SystemExit(images_to_s3())
    # SystemExit(test_access(settings.AWS_S3_BUCKET_NAME, 'basic_website/'))
    SystemExit(list_objects())

