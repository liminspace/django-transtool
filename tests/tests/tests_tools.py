import os
from django.conf import settings
from django.core.management import call_command
from tests.tests import CustomTestCase
from transtool.tools import get_lc_files_list, get_diff_po


class ToolsTestCase(CustomTestCase):
    def setUp(self):
        super(ToolsTestCase, self).setUp()
        self.clean_mo_files()

    def tearDown(self):
        self.clean_mo_files()
        super(ToolsTestCase, self).tearDown()

    def test_get_lc_files_list(self):
        def check_result(res):
            for item in res:
                self.assertTrue(isinstance(item, tuple))
                self.assertEqual(len(item), 2)
                self.assertTrue(os.path.isfile(item[0]))
                self.assertEqual(item[0], os.path.join(settings.BASE_DIR, item[1]))

        r = get_lc_files_list(settings.BASE_DIR)
        self.assertTrue(isinstance(r, list))
        self.assertEqual(len(r), 8)
        check_result(r)

        r = get_lc_files_list(settings.BASE_DIR, exts=('.po',))
        self.assertEqual(len(r), 8)
        check_result(r)

        r = get_lc_files_list(settings.BASE_DIR, exts=('.mo',))
        self.assertEqual(len(r), 0)
        check_result(r)

        call_command('transtool_compilemessages')

        r = get_lc_files_list(settings.BASE_DIR)
        self.assertEqual(len(r), 16)
        check_result(r)

        r = get_lc_files_list(settings.BASE_DIR, exts=('.mo',))
        self.assertEqual(len(r), 8)
        check_result(r)

    def test_get_diff_po(self):
        self.assertEqual(
            get_diff_po(os.path.join(settings.BASE_DIR, 'apps', 'app1', 'locale', 'en', 'LC_MESSAGES', 'django.po'),
                        os.path.join(settings.BASE_DIR, 'locale', 'en', 'LC_MESSAGES', 'django.po')),
            8
        )

        self.assertEqual(
            get_diff_po(os.path.join(settings.BASE_DIR, 'apps', 'app1', 'locale', 'en', 'LC_MESSAGES', 'django.po'),
                        os.path.join(settings.BASE_DIR, 'apps', 'app1', 'locale', 'en', 'LC_MESSAGES', 'djangojs.po')),
            6
        )

        self.assertEqual(
            get_diff_po(os.path.join(settings.BASE_DIR, 'apps', 'app1', 'locale', 'en', 'LC_MESSAGES', 'django.po'),
                        os.path.join(settings.BASE_DIR, 'apps', 'app1', 'locale', 'en', 'LC_MESSAGES', 'django.po')),
            0
        )
