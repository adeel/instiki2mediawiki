from distutils.core import setup

setup(
  name='instiki2mediawiki',
  version='0',
  description="migration script from Instiki to Mediawiki",
  author='Adeel Khan',
  author_email='kadeel@gmail.com',
  packages=['instiki2mediawiki'],
  scripts=['bin/instiki2mediawiki'],
  install_requires=['optparse', 'sqlalchemy'],
  license='MIT',
)