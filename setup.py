import os
from distutils.core import setup
from setuptools import find_packages
import transtool


setup(
    name='django-transtool',
    version=transtool.__version__,
    description='Make translating your django project easier.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license='MIT',
    author='Igor Melnyk @liminspace',
    author_email='liminspace@gmail.com',
    url='https://github.com/liminspace/django-transtool',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,  # because include static
    install_requires=[
        'django>=1.8,<2.1',
        'django-rosetta>=0.7.14',
        'requests>=2.15.1',
        'polib>=1.1.0',
    ],
    keywords=[
        'django', 'django-transtool', 'translation', 'localization', 'internationalization', 'i18n', 'l10n',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ],
)
