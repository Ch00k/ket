[![Build
Status](https://travis-ci.org/Ch00k/ket.svg?branch=master)](https://travis-ci.org/Ch00k/ket)

# ket

ket is a command-line tool, that makes interaction with
[Bitbucket](https://bitbucket.org) repositories easier.

You probably know [hub](https://github.com/github/hub) for
[GitHub](https://github.com) and/or
[lab](https://github.com/zaquestion/lab) for [GitLab](https://gitlab.com).
Well, ket is trying to accomplish the same goal, but for
[Bitbucket](https://bitbucket.org).

ket is currently only capable of managing pull requests. More to come!

## Installation
```
$ pip install ket
```

## Configuration
In order to interact with a Bitbucket repository, ket needs to authenticate to
Bitbucket with a username and an API key. The username is usually your
Bitbucket username. For the API key you should use the so-called app password.
More on app passwords, and how to create them
[here](https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html).

### Configuration file
ket tries to read its configuration from the file `$HOME/.config/ket`, which
must be formatted as follows:
```
[bitbucket]
username = Ch00k
api_key = <app_password>
```

## Running
```
$ ket
Usage: ket [OPTIONS] COMMAND [ARGS]...

  Bitbucket in your command-line

Options:
  --help  Show this message and exit.

Commands:
  pull-request  Pull request operations
```
```
$ ket pull-request
Usage: ket pull-request [OPTIONS] COMMAND [ARGS]...

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
```

## Tab completion
To enable tab completion, execute
```
eval "$(_KET_COMPLETE=source ket)"
```
