import os
from django.conf import settings
from django.test import TestCase


class CustomTestCase(TestCase):
    def _clean_files_with_ext(self, exts):
        for root, dirs, files in os.walk(settings.BASE_DIR):
            for file in files:
                if os.path.splitext(file)[1] in exts:
                    os.remove(os.path.join(root, file))

    def clean_mo_files(self):
        self._clean_files_with_ext(('.mo',))
