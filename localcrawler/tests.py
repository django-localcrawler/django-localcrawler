from django.test import TestCase
from localcrawler import settings
from localcrawler.core import Crawler


class LocalcrawlerTestCase(TestCase):
    
    ignore = []
    
    def test_localcrawler(self):
        
        crawler = Crawler(
            entry_point=settings.ENTRY_POINT,
            media=settings.CHECK_MEDIA,
            css=settings.CHECK_CSS,
            js=settings.CHECK_JS,
            bad_soup=settings.FAIL_ON_BAD_SOUP,
            ignore=self.ignore,
            client=self.client,
        )
        success = crawler.crawl()
        self.assertTrue(success, "At least one URL failed to load")
