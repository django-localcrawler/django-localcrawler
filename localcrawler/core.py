from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.test.client import Client
import sys

__all__ = ['Crawler']

class Crawler(object):
    def __init__(self, entry_point='/',
                 img=True, media=True,  # Media is deprecated: Use img
                 media_dir=True, static_dir=True, css=True, js=True,
                 bad_soup=True, client=None, ignore=None,
                 return_results=False, return_response=False,
                 output=sys.stderr):
        
        self.queue = []
        self.results = []
        ignore = ignore or []
        self.ignore = set(ignore) or set()

        self.entry_point = entry_point
        self._add_to_queue(entry_point)
        self.img = img
        self.media = media  # Deprecated. Use img
        self.media_dir = media_dir
        self.static_dir = static_dir
        self.css = css
        self.js = js
        self.bad_soup = bad_soup
        self.return_results = return_results
        self.return_response = return_response
        self.client = client or Client()
        self.output = output
        self.success = True
        self.crawled = 0
        self.failed = 0
        self.succeeded = 0
        
    def crawl(self):
        while self.queue:
            self.check(self.queue.pop(0))
        return self.success
            
    def check(self, url):
        """
        Open a single URL and check it's status code.
        
        If status is OK, run a scan if content type is html.
        """
        
        response = self.client.get(url, follow=True)
        
        # Add checked url to the results list
        # If return_response is set then also store the whole response
        if self.return_results:
            if self.return_response:
                result = (url, response.status_code, response)
            else:
                result = (url, response.status_code)
            self.results.append(result)
            
        self.crawled += 1
        
        # check if we're a 200
        if response.status_code != 200:
            self.success = False
            self.report(response.status_code, url, "URL Failed")
            return
        self.succeeded += 1
        if hasattr(response, 'render'):
            response.render()
        html = getattr(response, 'content', None)
        if html is None:
            html = getattr(response, 'streaming_content', '')
        if response.get('Content-Type', '').startswith('text/html'):
            self.scan(html, url)
            
    def report(self, prefix, url, message):
        self.failed += 1
        print >>self.output, "[%s] %s (%s)" % (prefix, url, message)
            
    def scan(self, html, url):
        """
        Scan a HTML document for further links we might be interested in.
        """
        try:
            soup = BeautifulSoup(html)
        except Exception, e:
            if self.bad_soup:
                self.success = False
                self.report("SOUP", url, unicode(e))
            return
        
        # media is deprecated but currently setting either media or
        # img to False will disable checking of images
        if self.img and self.media:
            self._parse_and_queue_if_valid(
                tags=soup.findAll('img'),
                attr='src',
            )
            
        if self.js:
            self._parse_and_queue_if_valid(
                tags=soup.findAll('script',attrs={'type': 'text/javascript'}),
                attr='src',
            )
            
        if self.css:
            self._parse_and_queue_if_valid(
                tags=soup.findAll('link', attrs={'type': 'text/css'}),
                attr='href',
            )
            
        self._parse_and_queue_if_valid(
            tags=soup.findAll('a'),
            attr='href',
        )
        
    def _add_to_queue(self, url):
        self.queue.append(url)
        # Add the url to the ignore list so we don't add it again
        self.ignore.add(url)
    
    def _parse_and_queue_if_valid(self, tags, attr):
        
        for tag in tags:
            
            url = tag.get(attr, '')
            url_parts = urlparse(url)
            
            valid = (
                url and
                url_parts.netloc == '' and
                url.startswith('/') and
                url not in self.ignore
            )
            if not self.media_dir and url.startswith(settings.MEDIA_URL):
                valid = False
            if not self.static_dir and url.startswith(settings.STATIC_URL):
                valid = False
            
            if valid:
                self._add_to_queue(url)

