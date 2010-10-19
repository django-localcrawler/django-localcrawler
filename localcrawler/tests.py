from django.test import TestCase
from localcrawler import settings
from localcrawler.core import Crawler


class LocalcrawlerTestCase(TestCase):
    def test_localcrawler(self):
        crawler = Crawler(settings.ENTRY_POINT, settings.CHECK_MEDIA,
                          settings.CHECK_CSS, settings.CHECK_JS,
                          settings.FAIL_ON_BAD_SOUP, self.client)
        success = crawler.crawl()
        self.assertTrue(success, "At least one URL failed to load")