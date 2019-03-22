from unittest import mock

from click.testing import CliRunner

from ket import cli

HELP_KET = """Usage: ket [OPTIONS] COMMAND [ARGS]...

  Bitbucket in your command-line

Options:
  --help  Show this message and exit.

Commands:
  pull-request  Pull request operations
"""


HELP_KET_PULL_REQUEST = """Usage: ket pull-request [OPTIONS] COMMAND [ARGS]...

  Pull request operations

Options:
  --help  Show this message and exit.

Commands:
  approve    Approve a pull request
  checkout   Checkout the branch of a pull request
  close      Close (decline) a pull request
  create     Create a pull request
  diff       Show the diff of a pull request
  list       List pull requests
  merge      Merge (accept) a pull request
  show       Show pull request details
  unapprove  Unapprove a pull request
"""


@mock.patch('ket.repo.Repo.__init__')
@mock.patch('ket.utils.get_bitbucket_auth_credentials')
def test_ket(get_credentials, init):
    init.return_value = None
    runner = CliRunner()
    res = runner.invoke(cli.ket)
    assert not res.stderr_bytes
    assert res.stdout == HELP_KET
    get_credentials.assert_not_called()
    init.assert_not_called()


@mock.patch('ket.repo.Repo.__init__')
@mock.patch('ket.utils.get_bitbucket_auth_credentials')
def test_ket_pull_request(get_credentials, init):
    init.return_value = None
    get_credentials.return_value = ('foo', 'bar')
    runner = CliRunner()
    res = runner.invoke(cli.ket, ['pull-request'])
    assert not res.stderr_bytes
    assert res.stdout == HELP_KET_PULL_REQUEST
    get_credentials.assert_called_once()
    init.assert_called_once_with(
        bitbucket_username='foo',
        bitbucket_api_key='bar')
