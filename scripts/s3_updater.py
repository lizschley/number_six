'''
    Update S3 using the StaticFiles class which inherites from AwsAutomater

    Goal: upload images. No longer updating other static files, but some remnents may remain.

    Note - images are not versioned.

    Run -> python scripts/s3_updater.py
'''
from common_classes.image_upload import ImageUpload
import settings


def images_to_s3():
    importer = ImageUpload()
    importer.image_uploader()


def test_access(bucket_name=settings.AWS_S3_BUCKET_NAME, prefix=None):
    importer = ImageUpload()
    importer.test_credentials(bucket_name, prefix)


def test_check(key):
    importer = ImageUpload()
    res = importer.check_load(key)
    print(res)


if __name__ == '__main__':
    SystemExit(images_to_s3())
    # SystemExit(test_access(settings.AWS_S3_BUCKET_NAME, 'basic_website/'))
    # SystemExit(test_check('basic_website/home_plant_images/non_native/red_clov'))
 