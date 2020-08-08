"""Contains the wrapper class for Tinder-API.
"""


from application.sources.pytinder.tinder_api import TinderAPI
from application.sources.pytinder.user import User, RateLimited, Match
from application.sources.pytinder.profile import Profile
from application.sources.pytinder.exceptions import InitializationError, RecsTimeout
from cached_property import cached_property
from time import time


class Session:
    """Class-wrapper for Tinder API.
    """
    def __init__(self, XAuthToken=None, config=None):
        """The constructor of a tinder-session:

        :param XAuthToken: tinder's x-auth-token (None by default)
        :param config: session's config-dict (None by default)
        """
        if XAuthToken is None and config is None:
            raise InitializationError("XAuthToken or configuration file (config.yaml) should be initialized.")
        self._api = TinderAPI(x_auth_token=XAuthToken)

        if XAuthToken is None:
            self._config = config
            self._api.auth(self._config['facebook_email'], self._config['facebook_password'])

    @cached_property
    def profile(self):
        """Set your tinder's profile.

        :return: parsed profile
        """
        return Profile(self._api.profile(), self._api)

    def nearby_users(self, limit=10):
        """Obtain users until a session won't abruptly aborted.

        :param limit: request limit (10 by default)
        :yield: User's profile
        """
        while True:
            response = self._api.recs(limit)

            if 'message' in response and response['message'] == 'recs timeout':
                raise RecsTimeout("Time of obtaining an user is out.")

            users = response['results'] if 'results' in response else []
            for user in users:
                if not user["_id"].startswith("tinder_rate_limited_id_"):
                    yield User(user, self)
                else:
                    yield RateLimited(user, self)
            if not len(users):
                break

    def update_profile(self, profile):
        """If you wish to update your profile.
        Description, Gender etc.

        :param profile: updated profile
        :return: response
        """
        return self._api.update_profile(profile)

    def update_location(self, latitude, longitude):
        """Update location.

        :param latitude: new latitude
        :param longitude: new longitude
        :return: response
        """
        return self._api.ping(latitude, longitude)

    def matches(self, since=None):
        """Obtains your matches.

        :param since: search for since when (None by default)
        :return: matches
        """
        response = self._api.matches(since)
        return (Match(match, self) for match in response if 'person' in match)

    def updates(self, since=None):
        """Check for updates (if somebody match you)

        :param since: search for since when (None by default)
        :return: matches
        """
        response = self._api.updates(since)
        return (Match(match, self) for match in response["matches"] if 'person' in match)

    @property
    def likes_remaining(self):
        """Check how many likes remaining.

        :return: remaining number of likes
        """
        return self._api.meta()['rating']['likes_remaining']

    @property
    def super_likes_remaining(self):
        """Check how many superlikes (stars) remaining.

        :return: remaining number of superlikes
        """
        return self._api.meta()['rating']['super_likes']['remaining']

    @property
    def can_like_in(self):
        """Return the number of seconds before being allowed to issue likes

        :return: number of seconds
        """
        now = int(time())
        limited_until = self._api.meta()['rating'].get('rate_limited_until', now)
        return limited_until / 1000 - now

    @property
    def banned(self):
        """Check if a profile is banned.

        :return: is profile banned
        """
        return self.profile.banned

