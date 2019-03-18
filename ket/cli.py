import sys

import click

from tabulate import tabulate

from . import repo, utils


@click.group()
@click.pass_context
def ket(ctx):
    """Bitbucket in your command-line"""
    ctx.ensure_object(dict)
    ctx.obj['r'] = None
    ctx.obj['err'] = None
    bb_username, bb_api_key = utils.get_bitbucket_auth_credentials()
    try:
        r = repo.Repo(
            bitbucket_username=bb_username,
            bitbucket_api_key=bb_api_key)
    except repo.RepoError as e:
        ctx.obj['err'] = e
    else:
        ctx.obj['r'] = r


@ket.group()
@click.pass_context
def pull_request(ctx):
    """Pull request operations"""


@pull_request.command()
@click.option(
    '-s', '--state', multiple=True, default=('open',), show_default=True,
    # TODO: There is also a `superseded` state
    type=click.Choice(['all', 'open', 'merged', 'declined', 'superseded']),
    help='Show only pull requests with state. Multiple values allowed')
@click.pass_context
def list(ctx, state):
    """List pull requests"""
    utils.check_err(ctx)
    data, headers = ctx.obj['r'].list_pull_requests(state)
    click.echo(tabulate(data, headers))


@pull_request.command()
@click.pass_context
@click.argument('id')
def show(ctx, id):
    """Show pull request details"""
    utils.check_err(ctx)
    try:
        res = ctx.obj['r'].get_pull_request(id)
    except repo.RepoError as e:
        click.echo(e, err=True)
        sys.exit(1)
    click.echo(tabulate(res))


@pull_request.command()
@click.option(
    '-t', '--target-branch', default='master', show_default=True,
    help='Pull request target branch')
@click.option(
    '-m', '--message', multiple=True, default=None, show_default=True,
    help=(
        'Pull request message. If multiple values provided, '
        'the first becomes the title, the rest form the description. '
        'If the option is omitted, the message can be edited in '
        'the default git editor'))
@click.pass_context
def create(ctx, target_branch, message):
    """Create a pull request"""
    utils.check_err(ctx)
    try:
        res = ctx.obj['r'].create_pull_request(
            target_branch=target_branch,
            message=message)
    except repo.RepoError as e:
        click.echo(e, err=True)
        sys.exit(1)
    click.echo(res)


@pull_request.command()
@click.pass_context
@click.argument('id')
def close(ctx, id):
    """Close (decline) a pull request"""
    utils.check_err(ctx)
    try:
        ctx.obj['r'].close_pull_request(id)
    except repo.RepoError as e:
        click.echo(e, err=True)
        sys.exit(1)


@pull_request.command()
@click.pass_context
@click.argument('id')
def merge(ctx, id):
    """Merge (accept) a pull request"""
    utils.check_err(ctx)
    try:
        ctx.obj['r'].merge_pull_request(id)
    except repo.RepoError as e:
        click.echo(e, err=True)
        sys.exit(1)


@pull_request.command()
@click.pass_context
@click.argument('id')
def approve(ctx, id):
    """Approve a pull request"""
    utils.check_err(ctx)
    try:
        ctx.obj['r'].approve_pull_request(id)
    except repo.RepoError as e:
        click.echo(e, err=True)
        sys.exit(1)


@pull_request.command()
@click.pass_context
@click.argument('id')
def unapprove(ctx, id):
    """Unapprove a pull request"""
    utils.check_err(ctx)
    try:
        ctx.obj['r'].unapprove_pull_request(id)
    except repo.RepoError as e:
        click.echo(e, err=True)
        sys.exit(1)


@pull_request.command()
@click.pass_context
@click.argument('id')
def diff(ctx, id):
    """Show the diff of a pull request"""
    utils.check_err(ctx)
    try:
        res = ctx.obj['r'].get_pull_request_diff(id)
    except repo.RepoError as e:
        click.echo(e, err=True)
        sys.exit(1)
    click.echo(res)


@pull_request.command()
@click.pass_context
@click.argument('id')
def checkout(ctx, id):
    """Checkout the branch of a pull request"""
    utils.check_err(ctx)
    try:
        ctx.obj['r'].checkout_pull_request_branch(id)
    except repo.RepoError as e:
        click.echo(e, err=True)
        sys.exit(1)
