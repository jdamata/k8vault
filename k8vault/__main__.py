#!/usr/bin/env python3

import click
import logging

@click.command()
@click.version_option()
def k8vault():
    pass

if __name__ == '__main__':
    k8vault()
