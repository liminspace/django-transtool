import os
import sys
import tempfile
import zipfile
import requests
from io import BytesIO
from polib import pofile
from django.core.management import CommandError, BaseCommand
from ...tools import get_lc_files_list, get_diff_po, timestamp_with_timezone
from ...settings import TRANSTOOL_DL_URL, TRANSTOOL_DL_KEY, TRANSTOOL_PROJECT_BASE_DIR


class Command(BaseCommand):
    help = ('Import locale messages from remote server. '
            '(You need configure TRANSTOOL_DL_URL and TRANSTOOL_DL_KEY settings)')

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--diff', action='store_true', default=False,
                            help='Only show difference.')
        parser.add_argument('--mo-only', action='store_true', default=False,
                            help='Import only mo-files.')
        parser.add_argument('--po-only', action='store_true', default=False,
                            help='Import only po-files.')

    @staticmethod
    def _get_diff_info(imp_zip_file, exts):
        result = {
            'changed': {},  # {rel path: number of changes}
            'new': [],  # rel path
            'del': [],  # rel path
            'ok': [],  # rel path
        }
        z = zipfile.ZipFile(imp_zip_file)
        try:
            for z_rel_path in z.namelist():
                abs_path = os.path.join(TRANSTOOL_PROJECT_BASE_DIR, z_rel_path)
                if not os.path.exists(abs_path):
                    result['new'].append(z_rel_path)
                else:
                    remote_file_content = z.read(z_rel_path)
                    ext = os.path.splitext(z_rel_path)[1]
                    if ext == '.po':
                        tmp_fd, remote_file_tmp_fn = tempfile.mkstemp(suffix='transtool')
                        try:
                            open(remote_file_tmp_fn, 'wb').write(remote_file_content)
                            d = get_diff_po(remote_file_tmp_fn, abs_path)
                            if d:
                                result['changed'][z_rel_path] = d
                            else:
                                result['ok'].append(z_rel_path)
                        finally:
                            os.close(tmp_fd)
                            os.remove(remote_file_tmp_fn)
                    elif ext == '.mo':
                        with open(abs_path, 'rb') as f:
                            local_file_content = f.read()
                        if remote_file_content != local_file_content:
                            result['changed'][z_rel_path] = None
                        else:
                            result['ok'].append(z_rel_path)
        finally:
            z.close()
        for abs_path, rel_path in get_lc_files_list(TRANSTOOL_PROJECT_BASE_DIR, exts=exts):
            if rel_path not in result['changed'] and rel_path not in result['ok']:
                result['del'].append(rel_path)
        return result

    def print_diff_info(self, diff_info):
        self.stdout.write('New files:')
        if diff_info['new']:
            for fn in sorted(diff_info['new']):
                self.stdout.write('  + {}'.format(fn))
        else:
            self.stdout.write('  :empty:')

        self.stdout.write('Changed files:')
        if diff_info['changed']:
            for fn in sorted(diff_info['changed'].keys()):
                changes = diff_info['changed'][fn]
                if changes:
                    self.stdout.write('  * {} ({})'.format(fn, changes))
                else:
                    self.stdout.write('  * {}'.format(fn))
        else:
            self.stdout.write('  :empty:')

        self.stdout.write('Deleted files:')
        if diff_info['del']:
            for fn in sorted(diff_info['del']):
                self.stdout.write('  - {}'.format(fn))
        else:
            self.stdout.write('  :empty:')

    @classmethod
    def update_import_datetime(cls, fn):
        po = pofile(fn)
        po.metadata['X-Transtool-Imported'] = timestamp_with_timezone()
        po.save()

    def copy_files(self, diff_info, imp_zip_file):
        z = zipfile.ZipFile(imp_zip_file)
        try:
            if diff_info['new']:
                self.stdout.write('Copy new files:')
                for fn in sorted(diff_info['new']):
                    content = z.read(fn)
                    po_path = os.path.join(TRANSTOOL_PROJECT_BASE_DIR, fn)
                    ext = os.path.splitext(po_path)[1]
                    try:
                        with open(po_path, 'wb') as f:
                            f.write(content)
                        if ext == '.po':
                            self.update_import_datetime(po_path)
                    except IOError as e:
                        self.stdout.write(e.message)
                        self.stdout.write('  SKIP: {}'.format(fn))
                    else:
                        self.stdout.write('  + {}'.format(fn))

            if diff_info['changed']:
                self.stdout.write('Copy changed files:')
                for fn in sorted(diff_info['changed'].keys()):
                    changes = diff_info['changed'][fn]
                    if changes:
                        fn_info = '{} ({})'.format(fn, changes)
                    else:
                        fn_info = fn
                    content = z.read(fn)
                    po_path = os.path.join(TRANSTOOL_PROJECT_BASE_DIR, fn)
                    ext = os.path.splitext(po_path)[1]
                    try:
                        with open(po_path, 'wb') as f:
                            f.write(content)
                        if ext == '.po':
                            self.update_import_datetime(po_path)
                    except IOError as e:
                        self.stdout.write(e.message)
                        self.stdout.write('  SKIP: {}'.format(fn_info))
                    else:
                        self.stdout.write('  * {}'.format(fn_info))

            if diff_info['del']:
                self.stdout.write('Maybe you should remove files:')
                for fn in sorted(diff_info['del']):
                    self.stdout.write('  - {}'.format(fn))
        finally:
            z.close()

    def handle(self, *args, **options):
        if not TRANSTOOL_DL_URL or not TRANSTOOL_DL_KEY:
            raise CommandError('Please, set TRANSTOOL_DL_URL and TRANSTOOL_DL_KEY settings.')
        if options['mo_only'] and options['po_only']:
            raise CommandError('Use only --mo-only or --po-only but not both.')
        self.stdout.write('Download file: Send POST request to {}'.format(TRANSTOOL_DL_URL))
        r = requests.post(TRANSTOOL_DL_URL, {
            'key': TRANSTOOL_DL_KEY,
            'po-only': str(int(options['po_only'])),
            'mo-only': str(int(options['mo_only'])),
        }, stream=True)
        if r.status_code != 200:
            self.stdout.write('Request status code is not 200: {}'.format(r.status_code))
            self.stdout.write('Fail.', ending='\n\n')
            sys.exit(1)
        file_content = BytesIO()
        for chunk in r.iter_content(chunk_size=(16 * 1024)):
            file_content.write(chunk)
        file_content.seek(0, os.SEEK_END)
        file_content_size = file_content.tell()
        self.stdout.write('Downloaded file {} {} bytes'.format(r.headers['Content-Type'], file_content_size))
        if options['po_only']:
            exts = ['.po']
        elif options['mo_only']:
            exts = ['.mo']
        else:
            exts = ['.po', '.mo']
        diff_info = self._get_diff_info(file_content, exts)
        if options['diff']:
            self.print_diff_info(diff_info)
        else:
            self.copy_files(diff_info, file_content)
        self.stdout.write('Done.', ending='\n\n')
