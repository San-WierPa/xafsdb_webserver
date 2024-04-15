"""
backends.py
-----------------------
@author: Sebastian Paripsa
@email: paripsa@uni-wuppertal.de (or: sebastian.paripsa@gmail.com)
@linkedin: https://www.linkedin.com/in/sebastian-paripsa/
@git: https://github.com/San-WierPa
@orcid: https://orcid.org/0009-0000-3487-5399

SEO Tags:
---------
#SciCat #DatasetAutomation #Python #DataScience

Requirements:
-------------
- Python 3.10
- SciCat API access
- AWS-S3 access

"""

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
