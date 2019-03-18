import configparser
import os
import subprocess
import sys
import tempfile

import click


def read_config():
    config_file = os.path.expanduser('~/.config/ket')
    if not os.path.exists(config_file):
        return
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def get_bitbucket_auth_credentials():
    config = read_config()
    if config and 'bitbucket' in config:
        bitbucket_username = config['bitbucket'].get('username')
        bitbucket_api_key = config['bitbucket'].get('api_key')
        return bitbucket_username, bitbucket_api_key
    return None, None


def check_err(ctx):
    if ctx.obj['err']:
        click.echo(ctx.obj['err'], err=True)
        sys.exit(1)


# TODO: How bad is this? o.O
def edit_pull_request_message(editor):
    with tempfile.NamedTemporaryFile() as tmp:
        subprocess.run([editor, tmp.name])
        with open(tmp.name) as f:
            return f.readlines()


def parse_pull_request_message(data):
    data = iter(data)
    title = None
    description = ''
    while not title:
        try:
            line = next(data)
        except StopIteration:
            break
        if not line.startswith('#'):
            title = line.strip()
    while True:
        try:
            line = next(data)
        except StopIteration:
            break
        if not line.startswith('#'):
            description += line
    description = description.strip()
    return title, description or None
