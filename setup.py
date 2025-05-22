from distutils.core import setup

setup(
  name = 'fcollections',
  packages = ['fcollections'], 
  version = '0.1',
  description = 'collections with method chaining',
  author = 'Phillip Adkins',
  author_email = 'philchiladki@yahoo.com',
  url = 'https://github.com/PilCAki/fcollections.git', # use the URL to the github repo
  download_url = 'https://github.com/PilCAki/fcollections/tarball/0.1', # I'll explain this in a second
  keywords = ['chaining', 'functional', 'cytoolz', 'itertoolz'], # arbitrary keywords
  classifiers = [],
  extras_require={
    'dev': [
        'flake8>=7.0.0',
        'black>=23.0.0;python_version>="3.7"',  # Black supports Python 3.7+
        'isort>=5.0.0',
    ],
  },
)
