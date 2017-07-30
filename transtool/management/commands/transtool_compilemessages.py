import os
from django.core.management import BaseCommand, call_command
from ...settings import TRANSTOOL_LOCALE_PATHS


class Command(BaseCommand):
    help = 'Compile all locale .po files.'

    def handle(self, *args, **options):
        self.stdout.write('Compile all .po files...')
        for locale_path, locale_opts in TRANSTOOL_LOCALE_PATHS:
            locale_path = os.path.abspath(locale_path)
            os.chdir(locale_path)
            self.stdout.write('chdir {}'.format(locale_path))
            self.stdout.write('run compilemessages')
            call_command('compilemessages')
        self.stdout.write('Done.')
