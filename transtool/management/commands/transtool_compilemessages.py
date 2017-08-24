import os
from django.core.management import BaseCommand, call_command
from ...settings import TRANSTOOL_PROJECT_BASE_DIR


class Command(BaseCommand):
    help = 'Compile all locale .po files.'

    def handle(self, *args, **options):
        self.stdout.write('Compile all .po files...')
        os.chdir(TRANSTOOL_PROJECT_BASE_DIR)
        self.stdout.write('chdir {}'.format(TRANSTOOL_PROJECT_BASE_DIR))
        self.stdout.write('run compilemessages')
        # todo add supporting --use-fuzzy, --locale and --exclude args
        call_command('compilemessages')
        self.stdout.write('Done.')
