#!/usr/bin/env python3

import click
import logging
import platform

from .keyring import (add_kubeconfig, delete_kubeconfig, get_kubeconfig,
  list_kubeconfig, update_kubeconfig)

logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    logger.debug('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
@click.argument('kubeconfig', type=click.Path(exists=True))
def add(kubeconfig):
    add_kubeconfig(kubeconfig)

@cli.command()
@click.argument('configname')
def delete(configname):
    delete_kubeconfig(configname)

@cli.command()
@click.argument('configname')
def get(configname):
    get_kubeconfig(configname)

@cli.command()
def list():
    list_kubeconfig()

@cli.command()
@click.argument('configname')
@click.argument('kubeconfig', type=click.Path(exists=True))
def update(configname, kubeconfig):
    update_kubeconfig(configname, kubeconfig)

if __name__ == '__main__':
    cli()
