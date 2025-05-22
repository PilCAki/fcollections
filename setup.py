from setuptools import setup, find_packages

setup(
  name = 'fcollections',
  packages = find_packages(), 
  version = '0.1',
  description = 'collections with method chaining',
  author = 'Phillip Adkins',
  author_email = 'philchiladki@yahoo.com',
  url = 'https://github.com/PilCAki/fcollections.git',
  download_url = 'https://github.com/PilCAki/fcollections/tarball/0.1',
  keywords = ['chaining', 'functional', 'cytoolz', 'itertoolz'],
  classifiers = [],
  install_requires=[
    'cytoolz',
  ],
  python_requires='>=3.6',
)
