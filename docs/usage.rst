Usage
=====

Tests
-----

The easiest way to test your website is to run
`python manage.py test localcrawler` which will crawl your whole website
starting at / including css, javascript and media files.

The test will fail if any link is broken.

Command
-------

If you would like a more detailed output, you can run
`python manage.py localcrawler` which will also crawl your whole website
starting at / including css, javascript and media files and print the result to
your console at the end of the crawling.