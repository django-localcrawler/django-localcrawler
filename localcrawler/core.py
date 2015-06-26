from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.test.client import Client
import sys

__all__ = ['Crawler']

class Crawler(object):
    def __init__(self, entry_point='/', img=True,
                 media=True,  # Deprecated: Use img
                 media_dir=True, static_dir=True,
                 css=True, js=True, bad_soup=True,
                 client=None, ignore=None,
                 output=sys.stderr):
        
        self.queue = [entry_point]
        self.ignore = ignore or []
        self.img = img
        self.media = img  # Deprecated: use img
        self.media_dir = media_dir
        self.static_dir = static_dir
        self.css = css
        self.js = js
        self.bad_soup = bad_soup
        if client:
            self.client = client
        else:
            self.client = Client()
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
        self.ignore.append(url)
        # check if we're a 200
        if response.status_code != 200:
            self.success = False
            self.report(response.status_code, url, "URL Failed")
            return
        self.succeeded += 1
        html = response.content
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
        if self.img and self.media:
            for img in soup.findAll('img'):
                src = img.get('src', '')
                if self._relevant(src):
                    self.queue.append(src)
        if self.js:
            for js in soup.findAll('script', attrs={'type': 'text/javascript'}):
                src = js.get('src', '')
                if self._relevant(src):
                    self.queue.append(src)
        if self.css:
            for css in soup.findAll('link', attrs={'type': 'text/css'}):
                href = css.get('href', '')
                if self._relevant(href):
                    self.queue.append(href)
        for a in soup.findAll('a'):
            href = a.get('href', '')
            if self._relevant(href):
                self.queue.append(href)
        
    def _relevant(self, url):
        conditions = [
            url,
            url.startswith('/'),
            not url in self.ignore,
        ]
        if not self.media_dir:
            conditions.append(not url.startswith(settings.MEDIA_URL))
        if not self.static_dir:
            conditions.append(not url.startswith(settings.STATIC_URL))
        return all(conditions)
