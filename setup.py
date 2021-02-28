from setuptools import setup, find_packages

setup(
    name = 'econtextapi',
    version = "0.1.2",
    author = 'Jonathan Spalink',
    author_email = 'jspalink@info.com',
    description = 'The eContext API provides taxonomic classification of text content',
    packages = find_packages(), #econtextapi', 'econtextapi.bin', 'econtextapi.classify', 'econtextapi.density', 'econtextapi.keywords'],
    install_requires=[
        'requests'
    ],
  
    entry_points = {
          'console_scripts': [
              'econtext-api = econtextapi.main:main',
              'econtext-classify-keywords= econtextapi.bin.classifykeywords:main',
              'econtext-classify-social= econtextapi.bin.classifysocial:main',
              'econtext-classify-url= econtextapi.bin.classifyurl:main'
          ]
      }

)
