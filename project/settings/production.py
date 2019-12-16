# pylint: disable=wildcard-import,unused-wildcard-import
from .base import *  # noqa: F403, F401


INSTALLED_APPS.insert(6, 'storages')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ["DB_NAME"],
        'USER': os.environ["DB_USER"],
        'PASSWORD': os.environ["DB_PASSWORD"],
        'HOST': os.environ["DB_HOST"],
        'PORT': '3306',
        'OPTIONS': {
            # 'isolation_level': 'read committed',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

AWS_STORAGE_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'couponwebsite.storage_backends.MediaStorage'

allowed_hosts = os.environ["ALLOWED_HOSTS"].split(";")
ALLOWED_HOSTS = allowed_hosts
