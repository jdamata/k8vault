import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Version
VERSION = (HERE / "Version").read_text()

setup(
  name = 'k8vault',
  packages = ['k8vault'],
  version = VERSION,
  license = 'GPL3',
  description = 'k8vault is a tool to securely store and access kubernetes configuration files development environment.',
  long_description_content_type = 'text/markdown',
  long_description = README,
  author = 'Joel Damata',
  author_email = 'joel.damata94@gmail.com',
  url = 'https://github.com/jdamata',
  download_url = 'https://github.com/jdamata/k8s-vault/archive/{}.tar.gz'.format(VERSION),
  keywords = ['Kubernetes', 'Config', 'Vault'],
  install_requires=[
          'click',
      ],
    entry_points='''
        [console_scripts]
        k8vault = k8vault.__main__:k8vault
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
