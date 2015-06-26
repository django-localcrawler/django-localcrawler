from django.conf import settings

DEFAULTS = {
    'FAIL_ON_BAD_SOUP': True,
    'CHECK_MEDIA': True,  # Deprecated - use CHECK_IMG
    'CHECK_IMG': True,
    'CHECK_JS': True,
    'CHECK_CSS': True,
    'CHECK_STATIC_DIR': True,
    'CHECK_MEDIA_DIR': True,
    'ENTRY_POINT': '/',
}

__all__ = DEFAULTS.keys()

for key, value in DEFAULTS.items():
    globals()[key] = getattr(settings, 'LOCALCRAWLER_%s' % key, value)