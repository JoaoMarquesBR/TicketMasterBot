class gitResponse:
    def __init__(self, id, type, actor, repo, payload, public, created_at):
        self.id = id
        self.type = type
        self.actor = actor
        self.repo = repo
        self.payload = payload
        self.public = public
        self.created_at = created_at

    @classmethod
    def from_json(cls, json_data):
        actor_data = json_data['actor']
        repo_data = json_data['repo']
        payload_data = json_data['payload']

        actor = Actor(actor_data['id'], actor_data['login'], actor_data['display_login'],
                      actor_data['gravatar_id'], actor_data['url'], actor_data['avatar_url'])
        repo = Repo(repo_data['id'], repo_data['name'], repo_data['url'])
        payload = Payload(payload_data['repository_id'], payload_data['push_id'], payload_data['size'],
                          payload_data['distinct_size'], payload_data['ref'], payload_data['head'],
                          payload_data['before'], payload_data['commits'])

        return cls(json_data['id'], json_data['type'], actor, repo, payload,
                   json_data['public'], json_data['created_at'])


class Actor:
    def __init__(self, id, login, display_login, gravatar_id, url, avatar_url):
        self.id = id
        self.login = login
        self.display_login = display_login
        self.gravatar_id = gravatar_id
        self.url = url
        self.avatar_url = avatar_url


class Repo:
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url


class Payload:
    def __init__(self, **kwargs):
        self.repository_id = kwargs.get('repository_id')
        self.push_id = kwargs.get('push_id')
        self.size = kwargs.get('size')
        self.distinct_size = kwargs.get('distinct_size')
        self.ref = kwargs.get('ref')
        self.head = kwargs.get('head')
        self.before = kwargs.get('before')
        self.commits = kwargs.get('commits')
        self.branch = self.ref.replace('refs/heads/', '')
        self.branch = self.ref.lower()
