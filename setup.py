from setuptools import setup, find_packages

setup (
    name = 'eContext API SDK',
    version = "0.1.0",
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
              'econtext-classify-keywords= econtextapi.bin.classifykeywords',
              'econtext-classify-social= econtextapi.bin.classifysocial',
              'econtext-classify-url= econtextapi.bin.classifyurl'
          ]
      }

)
