API
===

:class:`localcrawler.core.Crawler`
----------------------------------

    :param string entry_point: Start URL of the crawler, defaults to '/'.
    :param boolean media: Switch for media (images) scanning, defaults to True.
    :param boolean css: Switch for css scanning, defaults to True.
    :param boolean js: Switch for Javascript scanning, defaults to True.
    :param boolean bad_soup: Switch to turn counting parser errors as fails off,
        defaults to True.
    :param client: Test client to use, uses the default Django test client if
        None.
    :type client: None or :class:`django.test.client.Client` instance.
    :param filelike output: File-like object to use for output, defaults to
        `sys.stderr`.
        
        
    Usually you do not have to call any method other than
    :meth:`localcrawler.core.Crawler.crawl` on your instance of
    :class:`localcrawler.core.Crawler`. The other methods are documented here as
    reference for developers wanting to contribute to localcrawler.
        
    .. py:method:: crawl()
    
        Starts crawling the website. Returns True if crawling was successful.
        
    .. py:method:: check(url)
    
        Checks a single URL and scans the output if it's text/html.
        
    .. py:method:: report(prefix, url, message)
    
        Reports a failure to internal counter and the output channel defined.
        
    .. py:method:: scan(html, url)
    
        Scan a HTML document for more URLs to check.
        
    .. py:method:: _relevant(url)
    
        Checks if a URL is relevant for further checking. `url` might be None.