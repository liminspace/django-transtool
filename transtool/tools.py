import difflib
import os
import re
import polib


lc_dir_re = re.compile(r'^.*?locale/[\w\-]{2,5}/LC_MESSAGES$')


def get_lc_files_list(search_root, exts=('.po', '.mo')):
    """
    Returns list of tuple (absolute path, relative path)
    """
    result = []
    for root, dirs, files in os.walk(search_root):
        rel_root = root[len(search_root):].strip('/')
        if not lc_dir_re.match(rel_root):
            continue
        for filename in files:
            if os.path.splitext(filename)[1] in exts:
                result.append((os.path.join(root, filename), os.path.join(rel_root, filename)))
    return result


def get_diff_po(po1_fn, po2_fn):
    po1_lines = []
    po2_lines = []
    for entry in sorted(polib.pofile(po1_fn), key=lambda obj: obj.msgid):
        po1_lines.append((
            u'msgid {}\n\n'
            u'msgstr {}\n\n'
        ).format(entry.msgid, entry.msgstr))
    for entry in sorted(polib.pofile(po2_fn), key=lambda obj: obj.msgid):
        po2_lines.append((
            u'msgid {}\n\n'
            u'msgstr {}\n\n'
        ).format(entry.msgid, entry.msgstr))
    added = removed = 0
    for diff_line in difflib.unified_diff(po1_lines, po2_lines):
        if diff_line.startswith('+++ ') or diff_line.startswith('--- ') or diff_line.startswith('@@ '):
            continue
        if diff_line.startswith('+'):
            added += 1
        elif diff_line.startswith('-'):
            removed += 1
    return added + removed


def get_commonpath(paths):
    split_paths = [path.split(os.sep) for path in paths]
    try:
        isabs, = set(p[:1] == os.sep for p in paths)
    except ValueError:
        raise ValueError("Can't mix absolute and relative paths")
    split_paths = [[c for c in s if c and c != os.curdir] for s in split_paths]
    s1 = min(split_paths)
    s2 = max(split_paths)
    common = s1
    for i, c in enumerate(s1):
        if c != s2[i]:
            common = s1[:i]
            break
    prefix = os.sep if isabs else ''
    return prefix + os.sep.join(common)
