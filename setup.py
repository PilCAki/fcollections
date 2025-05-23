from setuptools import setup, find_packages

setup(
  name = 'chaincollections',
  packages = find_packages(), 
  version = '0.1',
  description = 'Collections with method chaining for Python',
  author = 'Phillip Adkins',
  author_email = 'philchiladki@yahoo.com',
  url = 'https://github.com/PilCAki/chaincollections.git',
  download_url = 'https://github.com/PilCAki/chaincollections/tarball/0.1',
  keywords = ['chaining', 'functional', 'cytoolz', 'itertoolz'],
  classifiers = [],
  install_requires=[
    'cytoolz',
  ],
  python_requires='>=3.6',
)
