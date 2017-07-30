import base64
import hashlib
import os
import polib
import shutil
from io import BytesIO
from django.core.management import BaseCommand, call_command
from django.core.management.commands import makemessages
from ...settings import TRANSTOOL_LOCALE_PATHS, TRANSTOOL_LOCALES, TRANSTOOL_DEFAULT_DOMAINS


class CustomMakemessagesCommand(makemessages.Command):
    source_dirs = None
    ignored_source_dirs = None
    update_all = None

    def add_arguments(self, parser):
        super(CustomMakemessagesCommand, self).add_arguments(parser)
        parser.add_argument('--add-source-dir', action='append', dest='source_dirs',
                            default=[], metavar='SOURCE_DIR',
                            help='Source directories to search phrases.')
        parser.add_argument('--update-all', action='store_true', dest='update_all', default=False,
                            help="Update all .po files even without any changes.")
        parser.add_argument('--ignore-source-dir', action='append', dest='ignored_source_dirs',
                            default=[], metavar='IGNORED_SOURCE_DIR',
                            help='Ignored source directories to skip searching phrases.')

    def handle(self, *args, **options):
        self.source_dirs = [os.path.abspath(p) for p in (options['source_dirs'] or [])]
        self.ignored_source_dirs = [os.path.abspath(p) for p in (options['ignored_source_dirs'] or [])]
        self.update_all = options['update_all']
        super(CustomMakemessagesCommand, self).handle(*args, **options)

    def find_files(self, root):
        files = []
        for source_dir in self.source_dirs:
            files.extend(super(CustomMakemessagesCommand, self).find_files(source_dir.rstrip('\\/')))

        if self.ignored_source_dirs:
            _files = []
            for f in files:
                ignore = False
                for ignored_source_dir in self.ignored_source_dirs:
                    if os.path.commonpath([ignored_source_dir]) == os.path.commonpath([ignored_source_dir, f.path]):
                        ignore = True
                        break
                if not ignore:
                    _files.append(f)
            files = _files
            del _files

        files.sort()
        return files

    @staticmethod
    def _get_hash_of_po_file(pofile_fn):
        h = hashlib.sha512()
        for entry in polib.pofile(pofile_fn):
            h.update(base64.b64encode(entry.msgid.encode()))
            h.update(base64.b64encode(entry.msgstr.encode()))
        return h

    def write_po_file(self, potfile, locale):
        pofile_fn = os.path.join(os.path.dirname(potfile), locale, 'LC_MESSAGES', '{}.po'.format(self.domain))
        old_po_hash = old_file = None
        if not self.update_all and os.path.isfile(pofile_fn):
            old_po_hash = self._get_hash_of_po_file(pofile_fn)
            old_file = BytesIO()
            with open(pofile_fn, 'rb') as f:
                shutil.copyfileobj(f, old_file)

        super(CustomMakemessagesCommand, self).write_po_file(potfile, locale)

        if old_po_hash:
            new_po_hash = self._get_hash_of_po_file(pofile_fn)
            if new_po_hash.hexdigest() == old_po_hash.hexdigest():
                old_file.seek(0)
                with open(pofile_fn, 'wb') as f:
                    shutil.copyfileobj(old_file, f)


class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--update-all', action='store_true', dest='update_all', default=False,
                            help="Update all .po files even without any changes.")

    def handle(self, *args, **options):
        for locale_path, locale_opts in TRANSTOOL_LOCALE_PATHS:
            locale_path = os.path.abspath(locale_path)
            os.chdir(locale_path)
            self.stdout.write('chdir {}'.format(locale_path))
            for domain in sorted(locale_opts.keys()):
                domain_opts = locale_opts[domain]
                command_kwargs = {
                    'domain': domain,
                    'extensions': domain_opts.get('EXT', TRANSTOOL_DEFAULT_DOMAINS[domain]['EXT']),
                    'source_dirs': domain_opts['DIRS'],
                    'locale': TRANSTOOL_LOCALES,
                    'update_all': options['update_all'],
                }
                if domain_opts.get('REST', False):
                    command_kwargs['ignored_source_dirs'] = self._get_excluded_source_dirs_for_rest(domain)
                call_command(CustomMakemessagesCommand(), **command_kwargs)

    @staticmethod
    def _get_excluded_source_dirs_for_rest(domain):
        dirs = []
        for locale_path, locale_opts in TRANSTOOL_LOCALE_PATHS:
            if domain not in locale_opts:
                continue
            domain_opts = locale_opts[domain]
            if domain_opts.get('REST', False):
                continue
            dirs.extend(domain_opts.get('DIRS', []))
        return dirs
