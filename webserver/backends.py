from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = settings.MEDIA_LOCATION
    default_acl = "public-read"
    querystring_auth = False


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.MEDIA_LOCATION
    default_acl = "private"
    querystring_auth = True


class StaticsMediaStorage(S3Boto3Storage):
    location = settings.AWS_LOCATION
    default_acl = "public-read"
    querystring_auth = False
