from django.conf import settings

DEFAULTS = {
    'FAIL_ON_BAD_SOUP': True,
    'CHECK_MEDIA': True,
    'CHECK_JS': True,
    'CHECK_CSS': True,
    'ENTRY_POINT': '/',
}

__all__ = DEFAULTS.keys()

for key, value in DEFAULTS.items():
    globals()[key] = getattr(settings, 'LOCALCRAWLER_%s' % key, value)