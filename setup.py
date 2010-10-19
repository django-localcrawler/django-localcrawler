from setuptools import setup, find_packages
from localcrawler import __version__
 
setup(
    name='django-localcrawler',
    version=__version__,
    description="django-localcrawler",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='testing,django',
    author='Jonas Obrist',
    author_email='jonas.obrist@divio.ch',
    url='http://github.com/ojii/django-localcrawler',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Django>=1.2",
        "BeautifulSoup>=3.0.8.1",
    ]
)