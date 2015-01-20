pytest-blockage
===============

Disable network requests during a test run.

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
