django-transtool
===========

Make translating your django project easier.

|

Installation
------------

**Requirements:**

* django v1.8+
* django-rosetta

**\1\. Install** ``django-transtool``.

* Via pip::

  $ pip install django-transtool

* Via setuptools::

  $ easy_install django-transtool
  

 For install development version use ``git+https://github.com/liminspace/django-transtool.git@develop`` instead ``django-transtool``.

**\2\. Set up** ``settings.py`` **in your django project.** ::

  INSTALLED_APPS = (
    ...,
    'transtool',
  )
