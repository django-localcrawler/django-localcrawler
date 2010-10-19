try:
    from cStringIo import StringIO
except ImportError:
    from StringIO import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.test.simple import run_tests
from django.test.utils import teardown_test_environment, setup_test_environment
from localcrawler.core import Crawler
from localcrawler.tests import LocalcrawlerTestCase

class LocalcrawlerAppTestCase(TestCase):
    def assertSio(self, sio, *lines):
        siolines = [line for line in sio.getvalue().split('\n') if line]
        self.assertEqual(siolines, list(lines))
        
    def _test_type(self, name, ext=None):
        ext = ext or name
        crawler = Crawler('/fail_%s/' % name, **{name: False})
        self.assertTrue(crawler.crawl())
        self.assertEqual(crawler.failed, 0)
        self.assertEqual(crawler.succeeded, 1)
        sio = StringIO()
        crawler = Crawler('/fail_%s/' % name, output=sio, **{name: True})
        self.assertFalse(crawler.crawl())
        self.assertEqual(crawler.failed, 1)
        self.assertEqual(crawler.succeeded, 1)
        self.assertSio(sio, "[404] /media/does_not_exist.%s (URL Failed)" % ext)
        crawler = Crawler('/win_%s/' % name, **{name: True})
        self.assertTrue(crawler.crawl())
        self.assertEqual(crawler.failed, 0)
        self.assertEqual(crawler.succeeded, 2)
        crawler = Crawler('/win_%s/' % name, **{name: False})
        self.assertTrue(crawler.crawl())
        self.assertEqual(crawler.failed, 0)
        self.assertEqual(crawler.succeeded, 1)
                
    def test_01_full(self):
        self._fixture_teardown()
        teardown_test_environment()
        call_command('test', 'localcrawler')
        call_command('localcrawler')
        setup_test_environment()
        self._fixture_setup()
    
    def test_02_css(self):
        self._test_type('css')
        
    def test_03_media(self):
        self._test_type('media', 'jpg')
        
    def test_04_js(self):
        self._test_type('js')
        
    def test_05_bad_soup(self):
        crawler = Crawler('/fail_soup/', bad_soup=False)
        self.assertTrue(crawler.crawl())
        self.assertEqual(crawler.failed, 0)
        self.assertEqual(crawler.succeeded, 1)
        sio = StringIO()
        crawler = Crawler('/fail_soup/', bad_soup=True, output=sio)
        self.assertFalse(crawler.crawl())
        self.assertEqual(crawler.failed, 1)
        self.assertEqual(crawler.succeeded, 1)
        self.assertSio(sio, "[SOUP] /fail_soup/ (bad end tag: u\"</scr' + 'ipt>\", at line 11, column 88)")
        
    def test_06_links(self):
        crawler = Crawler('/first/')
        self.assertTrue(crawler.crawl())
        self.assertEqual(crawler.failed, 0)
        self.assertEqual(crawler.succeeded, 2)