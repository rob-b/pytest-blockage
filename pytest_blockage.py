import sys
if sys.version_info[0] < 3:
    import httplib
else:
    import http.client as httplib
import logging
import smtplib


logger = logging.getLogger(__name__)


class MockHttpCall(Exception):
    pass


class MockSmtpCall(Exception):
    pass


def block_http(whitelist):
    def whitelisted(self, host, *args, **kwargs):
        try:
            string_type = basestring
        except NameError:
            # python3
            string_type = str
        if isinstance(host, string_type) and host not in whitelist:
            logger.warning('Denied HTTP connection to: %s' % host)
            raise MockHttpCall(host)
        logger.debug('Allowed HTTP connection to: %s' % host)
        return self.old(host, *args, **kwargs)

    whitelisted.blockage = True

    if not getattr(httplib.HTTPConnection, 'blockage', False):
        logger.debug('Monkey patching httplib')
        httplib.HTTPConnection.old = httplib.HTTPConnection.__init__
        httplib.HTTPConnection.__init__ = whitelisted


def block_smtp(whitelist):
    def whitelisted(self, host, *args, **kwargs):
        if isinstance(host, basestring) and host not in whitelist:
            logger.warning('Denied SMTP connection to: %s' % host)
            raise MockSmtpCall(host)
        logger.debug('Allowed SMTP connection to: %s' % host)
        return self.old(host, *args, **kwargs)

    whitelisted.blockage = True

    if not getattr(smtplib.SMTP, 'blockage', False):
        logger.debug('Monkey patching smtplib')
        smtplib.SMTP.old = smtplib.SMTP.__init__
        smtplib.SMTP.__init__ = whitelisted


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--blockage', action='store_true',
                    help='Block network requests during test run')


def pytest_sessionstart(session):
    config = session.config
    if config.option.blockage:
        http_whitelist = []
        smtp_whitelist = []

        block_http(http_whitelist)
        block_smtp(smtp_whitelist)
