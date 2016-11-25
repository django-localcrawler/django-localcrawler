from django.core.management.base import BaseCommand
from ...core import Crawler
import sys
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        crawler = Crawler()
        start = time.time()
        crawler.crawl()
        end = time.time()
        duration = end - start
        print ""
        print "--------------------------"
        print "django-localcrawler report"
        print "--------------------------"
        print ""
        print "Entry Point: %s" % crawler.entry_point
        print "Duration:    %.1fs" % duration
        print "Crawled:     %s" % crawler.crawled
        print "Succeeded:   %s" % crawler.succeeded
        print "Failed:      %s" % crawler.failed
        print "Success:     %s" % crawler.success
        print ""
        return crawler.success