import requests


class Client:
    def __init__(self, username, api_key, repo_slug):
        if None in (username, api_key):
            raise BitbucketAuthError("Bitbucket authentication not configured")
        base_url = 'https://api.bitbucket.org/2.0'
        self.repo_url = f'{base_url}/repositories/{username}/{repo_slug}'
        self.session = requests.Session()
        self.session.auth = (username, api_key)

    def get_repo(self):
        url = f'{self.repo_url}'
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def list_branches(self):
        url = f'{self.repo_url}/refs/branches'
        resp = self.session.get(url)
        return resp.json()

    def get_branch(self, branch_name):
        url = f'{self.repo_url}/refs/branches/{branch_name}'
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def list_pull_requests(self, state=('open',)):
        url = f'{self.repo_url}/pullrequests'
        params = {'state': [s.upper() for s in state]}
        resp = self.session.get(url, params=params)
        return resp.json()

    def get_pull_request(self, pr_id):
        url = f'{self.repo_url}/pullrequests/{pr_id}'
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def create_pull_request(self, source_branch, target_branch, title,
                            description=None):
        data = {
            'title': title,
            'description': description,
            'source': {'branch': {'name': source_branch}},
            'target': {'branch': {'name': target_branch}}}
        url = f'{self.repo_url}/pullrequests'
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def close_pull_request(self, pr_id):
        url = f'{self.repo_url}/pullrequests/{pr_id}/decline'
        resp = self.session.post(url)
        resp.raise_for_status()

    def merge_pull_request(self, pr_id):
        url = f'{self.repo_url}/pullrequests/{pr_id}/merge'
        resp = self.session.post(url)
        resp.raise_for_status()

    def approve_pull_request(self, pr_id):
        url = f'{self.repo_url}/pullrequests/{pr_id}/approve'
        resp = self.session.post(url)
        resp.raise_for_status()

    def unapprove_pull_request(self, pr_id):
        url = f'{self.repo_url}/pullrequests/{pr_id}/approve'
        resp = self.session.delete(url)
        resp.raise_for_status()

    def get_pull_request_diff(self, pr_id):
        url = f'{self.repo_url}/pullrequests/{pr_id}/diff'
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.text


class BitbucketAuthError(Exception):
    pass
