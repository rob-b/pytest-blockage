pytest-blockage
===============

Disable SMTP and HTTP requests during a test run.

Based mainly on https://github.com/andymckay/nose-blockage; source is
available at https://github.com/rob-b/pytest-blockage

Installation
------------

The plugin can be installed via `pypi <https://pypi.python.org/pypi/pytest-blockage/>`_::

    $ pip install pytest-blockage


Usage
-----

To activate the plugin the ``--blockage`` parameter should be passed. e.g.::

    $ py.test package --blockage

You can whitelist specific hosts::

    $ py.test package --blockage --blockage-http-whitelist=some_site --blockage-smtp-whitelist=fake_smtp

Configuration
-------------

All settings can be stored in your pytest file, with the same variable names as
the argument names mentioned under usage::

    blockage=true
    blockage-http-whitelist=some_site
    blockage-smtp-whitelist=fake_smtp


