import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'test'

DEBUG = True

ALLOWED_HOSTS = ['*']

LANGUAGES = (
    ('en', 'English'),
    ('uk', 'Ukrainian'),
)

INSTALLED_APPS = (
    'transtool',
    'tests',
    'app1',
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'tests.urls'

WSGI_APPLICATION = 'tests.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3'),
        'NAME': ':memory:',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.request',
            ),
        },
    },
]

TRANSTOOL_DEFAULT_DOMAINS = {
    'django': {
        'EXT': ('html', 'txt', 'py'),
    },
    'djangojs': {
        'EXT': ('js',),
    },
    'djangotst': {
        'EXT': ('tst',)
    }
}

TRANSTOOL_LOCALE_PATHS = (
    (os.path.join(BASE_DIR, 'apps/app1/'), {
        'django': {
            'DIRS': (
                os.path.join(BASE_DIR, 'apps/app1/'),
                os.path.join(BASE_DIR, 'templates/app1/'),
            ),
            'EXT': ('html', 'txt', 'py', 'rml'),
        },
        'djangojs': {
            'DIRS': (
                os.path.join(BASE_DIR, 'static/app1/'),
            ),
            # 'EXT': ('js',),
        },
    }),
    (os.path.join(BASE_DIR, './'), {
        'django': {
            'DIRS': (
                BASE_DIR,
            ),
            'REST': True,
        },
        'djangojs': {
            'DIRS': (
                BASE_DIR,
            ),
            'REST': True,
        },
    }),
)

TRANSTOOL_DL_KEY = 'testkey'
TRANSTOOL_EXPORT_KEY = 'testkey'
