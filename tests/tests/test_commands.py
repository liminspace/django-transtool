import os
from django.conf import settings
from django.core.management import call_command
from tests.tests import CustomTestCase


class MakemessagesTestCase(CustomTestCase):
    def setUp(self):
        super(MakemessagesTestCase, self).setUp()
        self.clean_mo_files()

    def tearDown(self):
        self.clean_mo_files()
        super(MakemessagesTestCase, self).tearDown()

    # @mock.patch('transtool.management.commands.transtool_makemessages.CustomMakemessagesCommand')
    def test_default(self):
        # fn = os.path.join(settings.BASE_DIR, 'apps/app1/locale/en/LC_MESSAGES/django.po')

        # додати app3 в apps, static та templates і заігнорити його
        # створити динамічно там якісь файли (або скопіювати їх з інших)
        # підмінити опцію settings.TRANSTOOL_LOCALE_PATHS

        self._clean_files_with_ext('.po')
        call_command('transtool_makemessages')
        # print(custom_cmd)
