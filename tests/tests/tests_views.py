import zipfile
import os
from io import BytesIO
from django.conf import settings
from django.core.management import call_command
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from tests.tests import CustomTestCase


class ViewsTestCase(CustomTestCase):
    def setUp(self):
        super(ViewsTestCase, self).setUp()
        self.clean_mo_files()

    def tearDown(self):
        self.clean_mo_files()
        super(ViewsTestCase, self).tearDown()

    def _check_response(self, r, file_namelist=None):
        self.assertEqual(r.get('Content-Type'), 'application/zip')
        self.assertEqual(r.get('Content-Disposition'), 'attachment; filename="localemessages.zip"')
        if file_namelist is not None:
            file_namelist = list(file_namelist)
            content = BytesIO(r.content)
            z = zipfile.ZipFile(content)
            try:
                for z_rel_path in z.namelist():
                    self.assertIn(z_rel_path, file_namelist)
                    file_namelist.remove(z_rel_path)

                    z_file_content = z.read(z_rel_path)
                    with open(os.path.join(settings.BASE_DIR, z_rel_path), 'rb') as f:
                        self.assertTrue(z_file_content == f.read(), 'File {} is not equal with zip'.format(z_rel_path))

            finally:
                z.close()
            self.assertEqual(len(file_namelist), 0)

    def test_invalid_method(self):
        r = self.client.get(reverse('localemessages_export'), data={
            'key': settings.TRANSTOOL_DL_KEY + '1',
        })
        self.assertEqual(r.status_code, 404)

    def test_invalid_key(self):
        r = self.client.post(reverse('localemessages_export'), data={
            'key': settings.TRANSTOOL_DL_KEY + '1',
        })
        self.assertEqual(r.status_code, 403)

    def test_default(self):
        call_command('transtool_compilemessages')
        r = self.client.post(reverse('localemessages_export'), data={
            'key': settings.TRANSTOOL_DL_KEY,
        })
        self.assertEqual(r.status_code, 200)
        self._check_response(r, (
            'apps/app1/locale/en/LC_MESSAGES/django.po',
            'apps/app1/locale/en/LC_MESSAGES/django.mo',
            'apps/app1/locale/en/LC_MESSAGES/djangojs.po',
            'apps/app1/locale/en/LC_MESSAGES/djangojs.mo',
            'apps/app1/locale/uk/LC_MESSAGES/django.po',
            'apps/app1/locale/uk/LC_MESSAGES/django.mo',
            'apps/app1/locale/uk/LC_MESSAGES/djangojs.po',
            'apps/app1/locale/uk/LC_MESSAGES/djangojs.mo',
            'locale/en/LC_MESSAGES/django.po',
            'locale/en/LC_MESSAGES/django.mo',
            'locale/en/LC_MESSAGES/djangojs.po',
            'locale/en/LC_MESSAGES/djangojs.mo',
            'locale/uk/LC_MESSAGES/django.po',
            'locale/uk/LC_MESSAGES/django.mo',
            'locale/uk/LC_MESSAGES/djangojs.po',
            'locale/uk/LC_MESSAGES/djangojs.mo',
        ))

    def test_with_po_only(self):
        call_command('transtool_compilemessages')
        r = self.client.post(reverse('localemessages_export'), data={
            'key': settings.TRANSTOOL_DL_KEY,
            'po-only': '1',
        })
        self.assertEqual(r.status_code, 200)
        self._check_response(r, (
            'apps/app1/locale/en/LC_MESSAGES/django.po',
            'apps/app1/locale/en/LC_MESSAGES/djangojs.po',
            'apps/app1/locale/uk/LC_MESSAGES/django.po',
            'apps/app1/locale/uk/LC_MESSAGES/djangojs.po',
            'locale/en/LC_MESSAGES/django.po',
            'locale/en/LC_MESSAGES/djangojs.po',
            'locale/uk/LC_MESSAGES/django.po',
            'locale/uk/LC_MESSAGES/djangojs.po',
        ))

    def test_with_mo_only(self):
        r = self.client.post(reverse('localemessages_export'), data={
            'key': settings.TRANSTOOL_DL_KEY,
            'mo-only': '1',
        })
        self.assertEqual(r.status_code, 200)
        self._check_response(r, ())
