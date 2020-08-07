from application.sources.pytinder.tinder_api import TinderAPI
from application.sources.pytinder.user import User, RateLimited, Match
from application.sources.pytinder.profile import Profile
from application.sources.pytinder.exceptions import InitializationError, RecsTimeout
from cached_property import cached_property
from time import time


class Session:

    def __init__(self, XAuthToken=None, config=None):
        """The constructor of a tinder-session:

        :parameters
        config - the configuration of session retrieved from config.yaml file.
        """
        if XAuthToken is None and config is None:
            raise InitializationError("XAuthToken or configuration file (config.yaml) should be initialized.")
        self._api = TinderAPI(x_auth_token=XAuthToken)

        if XAuthToken is None:
            self._config = config
            self._api.auth(self._config['facebook_email'], self._config['facebook_password'])

    @cached_property
    def profile(self):
        return Profile(self._api.profile(), self._api)

    def nearby_users(self, limit=10):
        while True:
            response = self._api.recs(limit)

            if 'message' in response and response['message'] == 'recs timeout':
                raise RecsTimeout

            users = response['results'] if 'results' in response else []
            for user in users:
                if not user["_id"].startswith("tinder_rate_limited_id_"):
                    yield User(user, self)
                else:
                    yield RateLimited(user, self)
            if not len(users):
                break

    def update_profile(self, profile):
        return self._api.update_profile(profile)

    def update_location(self, latitude, longitude):
        return self._api.ping(latitude, longitude)

    def matches(self, since=None):
        response = self._api.matches(since)
        return (Match(match, self) for match in response if 'person' in match)

    def updates(self, since=None):
        response = self._api.updates(since)
        return (Match(match, self) for match in response["matches"] if 'person' in match)

    @property
    def likes_remaining(self):
        return self._api.meta()['rating']['likes_remaining']

    @property
    def super_likes_remaining(self):
        return self._api.meta()['rating']['super_likes']['remaining']

    @property
    def can_like_in(self):
        """
        Return the number of seconds before being allowed to issue likes
        """
        now = int(time())
        limited_until = self._api.meta()['rating'].get('rate_limited_until', now)
        return limited_until / 1000 - now

    @property
    def banned(self):
        return self.profile.banned

