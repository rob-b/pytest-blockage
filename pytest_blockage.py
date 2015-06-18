import sys
if sys.version_info[0] < 3:
    import httplib
else:
    import http.client as httplib
import logging


logger = logging.getLogger(__name__)


class MockHttpCall(Exception):
    pass


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--blockage', action='store_true',
                    help=u'Block network requests during test run')


def pytest_sessionstart(session):
    config = session.config
    if config.option.blockage:
        http_whitelist = []

        def whitelisted(self, host, *args, **kwargs):
            try:
                string_type = basestring
            except NameError:
                # python3
                string_type = str
            if isinstance(host, string_type) and host not in http_whitelist:
                logger.warning('Denied HTTP connection to: %s' % host)
                raise MockHttpCall(host)
            logger.debug('Allowed HTTP connection to: %s' % host)
            return self.old(host, *args, **kwargs)

        whitelisted.blockage = True

        if not getattr(httplib.HTTPConnection, 'blockage', False):
            logger.debug('Monkey patching httplib')
            httplib.HTTPConnection.old = httplib.HTTPConnection.__init__
            httplib.HTTPConnection.__init__ = whitelisted
