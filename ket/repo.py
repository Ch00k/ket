import functools

import git
import requests

from . import bitbucket, utils


class Repo:
    def __init__(self, bitbucket_username, bitbucket_api_key):
        try:
            self.git_repo = git.Repo()
        except git.InvalidGitRepositoryError:
            raise RepoError("Not a git repository")
        try:
            self.bitbucket_client = bitbucket.Client(
                username=bitbucket_username,
                api_key=bitbucket_api_key,
                repo_slug=self.slug)
        except bitbucket.BitbucketAuthError as e:
            raise RepoError(e)

    @property
    @functools.lru_cache()
    def slug(self):
        remote_url = self.git_repo.remote().url
        parts = remote_url.rsplit('/', 1)
        if len(parts) != 2:
            raise RuntimeError("Unable to extract repo slug from remote URI")
        repo_slug = parts[1]
        repo_slug = repo_slug.rsplit('.', 1)[0]  # cut off `.git` part
        return repo_slug

    def list_pull_requests(self, state=('open',)):
        # `all` is a hack. Invalid `state` query param makes Bitbucket respond
        # with all (i.e. unfiltered) items
        if 'all' in state:
            state = ('all',)
        try:
            res = self.bitbucket_client.list_pull_requests(state)
        except requests.HTTPError as e:
            raise RepoError(e)
        data = [(
            item['id'],
            item['state'].lower(),
            item['author']['display_name'],
            item['title'],
            item['links']['html']['href']) for item in res['values']]
        headers = ['ID', 'State', 'Author', 'Title', 'URL']
        return data, headers

    def get_pull_request(self, pr_id):
        try:
            res = self.bitbucket_client.get_pull_request(pr_id)
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 404:
                msg = f"Pull request {pr_id} not found"
            raise RepoError(msg)
        return [
            ('ID', res['id']),
            ('State', res['state'].lower()),
            ('Author', res['author']['display_name']),
            ('Title', res['title']),
            ('Description', res['description']),
            ('URL', res['links']['html']['href']),
            ('Source branch', res['source']['branch']['name']),
            ('Target branch', res['destination']['branch']['name']),
            ('Approvals', len(
                [p for p in res['participants'] if p['approved']]))]

    def create_pull_request(self, target_branch='master', message=None):
        self._verify_remote_repo_exists()
        source_branch = self.git_repo.active_branch.name
        if source_branch == target_branch:
            raise RuntimeError("Source and target branches must be different")
        try:
            self._verify_remote_branch_exists(source_branch)
        except RepoError as e:
            raise RepoError(f"{e}. Did you forget to push?")
        title, description = self._generate_pull_request_message(message)
        try:
            res = self.bitbucket_client.create_pull_request(
                source_branch=source_branch,
                target_branch=target_branch,
                title=title,
                description=description)
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 400:
                msg = e.response.json()['error']['message']
            raise RepoError(msg)
        return res['links']['html']['href']

    def close_pull_request(self, pr_id):
        try:
            self.bitbucket_client.close_pull_request(pr_id)
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 404:
                msg = f"Pull request {pr_id} not found"
            raise RepoError(msg)

    def merge_pull_request(self, pr_id):
        try:
            self.bitbucket_client.merge_pull_request(pr_id)
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 404:
                msg = f"Pull request {pr_id} not found"
            raise RepoError(msg)

    def approve_pull_request(self, pr_id):
        try:
            self.bitbucket_client.approve_pull_request(pr_id)
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 404:
                msg = f"Pull request {pr_id} not found"
            raise RepoError(msg)

    def unapprove_pull_request(self, pr_id):
        try:
            self.bitbucket_client.unapprove_pull_request(pr_id)
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 404:
                msg = f"Pull request {pr_id} not found"
            raise RepoError(msg)

    def get_pull_request_diff(self, pr_id):
        try:
            return self.bitbucket_client.get_pull_request_diff(pr_id)
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 404:
                msg = f"Pull request {pr_id} not found"
            raise RepoError(msg)

    def checkout_pull_request_branch(self, pr_id):
        pull_request = self.get_pull_request(pr_id)
        source_branch = pull_request['source']['branch']['name']
        self._verify_remote_branch_exists(source_branch)
        try:
            self.git_repo.remote().fetch(source_branch)
            self.git_repo.heads[source_branch].checkout()
        except git.exc.GitCommandError as e:
            # TODO: https://github.com/gitpython-developers/GitPython/pull/798
            raise RepoError(e.stderr.split("'")[1])

    def _verify_remote_repo_exists(self):
        try:
            self.bitbucket_client.get_repo()
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 404:
                msg = (
                    f"Bitbucket repository "
                    f"{self.bitbucket_client.username}/{self.slug} not found")
            raise RepoError(msg)

    def _verify_remote_branch_exists(self, branch_name):
        try:
            self.bitbucket_client.get_branch(branch_name)
        except requests.HTTPError as e:
            msg = e
            if e.response.status_code == 404:
                msg = f"Branch {branch_name} not found"
            raise RepoError(msg)

    def _generate_pull_request_message(self, message_cmd_option):
        if message_cmd_option:
            data = message_cmd_option
        else:
            editor = git.Git().var('GIT_EDITOR')
            data = utils.edit_pull_request_message(editor)
        title, description = utils.parse_pull_request_message(data)
        if not title:
            raise RepoError("Aborting (empty pull request title)")
        return title, description


class RepoError(Exception):
    pass
