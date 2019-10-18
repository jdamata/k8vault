import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Version
VERSION = open("Version").readline().rstrip()

setup(
  name = 'k8vault',
  packages = ['k8vault'],
  version = VERSION,
  long_description_content_type = 'text/markdown',
  long_description = README,
  license = 'GPL3',
  description = 'Store and access kubernetes configuration files',
  author = 'Joel Damata',
  author_email = 'joel.damata94@gmail.com',
  url = 'https://github.com/jdamata',
  download_url = 'https://github.com/jdamata/k8vault/archive/{}.tar.gz'.format(VERSION),
  keywords = ['Kubernetes', 'Config', 'Vault'],
  install_requires=[
          'click',
          'keyring',
          'pywin32',
      ],
    entry_points='''
        [console_scripts]
        k8vault = k8vault.__main__:cli
    ''',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)
