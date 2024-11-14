"""
Module variables that need to be available to use the app and particulary S3.
Note - there is some extra variables 
"""
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT = parent = os.path.dirname(BASE_DIR)
sys.path.append(parent)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('HASH_KEY')

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# Following is for S3 implementation
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'lizschley-static'
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = 'dirl4bhsg8ywj.cloudfront.net'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
# Trouble-shooting
AWS_QUERYSTRING_AUTH = False
AWS_S3_REGION_NAME = 'us-east-1'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
