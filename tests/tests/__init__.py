import os
from django.conf import settings
from django.test import TestCase


class CustomTestCase(TestCase):
    def clean_mo_files(self):
        for root, dirs, files in os.walk(settings.BASE_DIR):
            for file in files:
                if os.path.splitext(file)[1] in ('.mo',):
                    os.remove(os.path.join(root, file))
