from django.conf import settings

__all__ = ['FAIL_ON_BAD_SOUP', 'CHECK_MEDIA', 'CHECK_JS', 'CHECK_CSS', 'ENTRY_POINT']

DEFAULTS = {
    'FAIL_ON_BAD_SOUP': True,
    'CHECK_MEDIA': True,
    'CHECK_JS': True,
    'CHECK_CSS': True,
    'ENTRY_POINT': '/',
}

for key, value in DEFAULTS.items():
    globals()[key] = getattr(settings, 'LOCALCRAWLER_%s' % key, value)