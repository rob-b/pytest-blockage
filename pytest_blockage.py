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


def get_string_type():
    try:
        return basestring
    except NameError:  # python3
        return str


def block_http(whitelist):
    def whitelisted(self, host, *args, **kwargs):
        if isinstance(host, get_string_type()) and host not in whitelist:
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
        if isinstance(host, get_string_type()) and host not in whitelist:
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
    group = parser.getgroup('blockage')
    group.addoption('--blockage', action='store_true',
                    help='Block network requests during test run')
    parser.addini(
        'blockage', 'Block network requests during test run', default=False)

    group.addoption(
        '--blockage-http-whitelist',
        action='store',
        help='Do not block HTTP requests to this comma separated list of '
            'hostnames',
        default=''
    )
    parser.addini(
        'blockage-http-whitelist',
        'Do not block HTTP requests to this comma separated list of hostnames',
        default=''
    )

    group.addoption(
        '--blockage-smtp-whitelist',
        action='store',
        help='Do not block SMTP requests to this comma separated list of '
            'hostnames',
        default=''
    )
    parser.addini(
        'blockage-smtp-whitelist',
        'Do not block SMTP requests to this comma separated list of hostnames',
        default=''
    )


def pytest_sessionstart(session):
    config = session.config

    if config.option.blockage or config.getini('blockage'):
        http_whitelist_str = config.option.blockage_http_whitelist or config.getini('blockage-http-whitelist')
        http_whitelist = http_whitelist_str.split(',')

        smtp_whitelist_str = config.option.blockage_smtp_whitelist or config.getini('blockage-smtp-whitelist')
        smtp_whitelist = smtp_whitelist_str.split(',')

        block_http(http_whitelist)
        block_smtp(smtp_whitelist)
