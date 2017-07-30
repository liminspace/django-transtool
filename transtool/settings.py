from django.conf import settings


TRANSTOOL_DL_URL = getattr(settings, 'TRANSTOOL_DL_URL', None)  # http://example.com/localemessages/export/
TRANSTOOL_DL_KEY = getattr(settings, 'TRANSTOOL_DL_KEY', None)  # for import translates from remote server
TRANSTOOL_EXPORT_KEY = getattr(settings, 'TRANSTOOL_EXPORT_KEY', None)  # for export translates by http request
TRANSTOOL_PROJECT_BASE_DIR = getattr(settings, 'TRANSTOOL_PROJECT_BASE_DIR', settings.BASE_DIR)  # root dir of project
TRANSTOOL_LOCALES = getattr(settings, 'TRANSTOOL_LOCALES', tuple(map(lambda t: t[0], settings.LANGUAGES)))

TRANSTOOL_DEFAULT_DOMAINS = {
    'django': {
        'EXT': ('html', 'txt', 'py'),
    },
    'djangojs': {
        'EXT': ('js',),
    },
}

# update TRANSTOOL_DEFAULT_DOMAINS from project settings using addition method
for _domain, _opts in getattr(settings, 'TRANSTOOL_DEFAULT_DOMAINS', {}).items():
    if _domain in TRANSTOOL_DEFAULT_DOMAINS:
        # if domain is exists
        # just update options without remove default ones
        for _k, _v in _opts.items():
            TRANSTOOL_DEFAULT_DOMAINS[_domain][_k] = _v
    else:
        # add new domain
        TRANSTOOL_DEFAULT_DOMAINS[_domain] = _opts

# Example:
# TRANSTOOL_LOCALE_PATHS = (
#     (os.path.join(BASE_DIR, 'apps/myapp/'), {  # directory that contains locale subdirectory
#         'django': {
#             'DIRS': (
#                 os.path.join(BASE_DIR, 'apps/myapp/'),
#                 os.path.join(BASE_DIR, 'templates/myapp/'),
#             ),
#             # 'EXT': ('html', 'txt', 'py'),
#         },
#         'djangojs': {
#             'DIRS': (
#                 os.path.join(BASE_DIR, 'static/myapp/'),
#             ),
#             # 'EXT': ('js',),
#         },
#     }),
#     (os.path.join(BASE_DIR, './'), {
#         'django': {
#             'DIRS': (
#                 BASE_DIR,
#             ),
#             'REST': True,
#         },
#         'djangojs': {
#             'DIRS': (
#                 BASE_DIR,
#             ),
#             'REST': True,
#         },
#     }),
# )
TRANSTOOL_LOCALE_PATHS = getattr(settings, 'TRANSTOOL_LOCALE_PATHS', ())
