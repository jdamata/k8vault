#!/usr/bin/env python3

import click
import logging
import platform

from .add import *
from .get import *

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    logger.info('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
@click.argument('kubeconfig', type=click.Path(exists=True))
def add(kubeconfig):
    if platform.system() == "Darwin":
        add_darwin_kubeconfig(kubeconfig)
    elif platform.system() == "Windows":
        add_windows_kubeconfig(kubeconfig)
    elif platform.system() == "Linux":
        add_linux_kubeconfig(kubeconfig)

@cli.command()
@click.argument('configname')
def get(configname):
    if platform.system() == "Darwin":
        get_darwin_kubeconfig(configname)
    elif platform.system() == "Windows":
        get_windows_kubeconfig(configname)
    elif platform.system() == "Linux":
        get_linux_kubeconfig(configname)

if __name__ == '__main__':
    cli()
