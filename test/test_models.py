from django.test import TestCase
from xafsdb_web.models import Files

from webserver.backends import PrivateMediaStorage


class FilesModelTest(TestCase):
    """
    Test
    """

    def setUp(self):
        self.file = Files.objects.create(dataset_id="test123", file_name="test.txt")

    def test_file_name(self):
        self.assertEqual(str(self.file), "test.txt")
