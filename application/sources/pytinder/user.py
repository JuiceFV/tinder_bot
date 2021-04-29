"""Contains the classes responsible for an User.
User is the profile differs from yours.
"""


import itertools
import dateutil
import datetime
from application.sources.pytinder.exceptions import UserInitializationError
from application.sources.pytinder.globals import GENDER_MAP, VALID_PHOTO_SIZES
from application.sources.pytinder.message import Message
import six


class User:
    """The user-class.
    Parse the user's information.
    And responsible for the interaction your profile with user profile.
    """
    def __init__(self, profile_json, session):
        """The user definition.

        :param profile_json: an user's profile in the json format.
        :param session: a session
        """
        try:
            self._session = session
            self.id = profile_json['_id']
            self._photos = profile_json['photos']
            self.birth_date = dateutil.parser.parse(profile_json['birth_date'])
            self.schools = []
            self.jobs = []
            self.name = profile_json['name']
            self.bio = profile_json['bio']
            self.ping_time = profile_json['ping_time']
            try:
                self.schools.extend(["%s" % school["name"] for school in profile_json['schools'] if 'name' in school])
                self.jobs.extend(["%s @ %s" % (job["title"]["name"], job["company"]["name"]) for job in profile_json['jobs'] if 'title' in job and 'company' in job])
                self.jobs.extend(["%s" % (job["company"]["name"],) for job in profile_json['jobs'] if 'title' not in job and 'company' in job])
                self.jobs.extend(["%s" % (job["title"]["name"],) for job in profile_json['jobs'] if 'title' in job and 'company' not in job])
            except (ValueError, KeyError):
                pass
            self._profile_json_format = profile_json
        except UserInitializationError:
            print("The initialization of a user has went wrong.\nPerhaps the profile you passed is incorrect.")

    @property
    def instagram_username(self):
        """Obtain instagram username if it exists.

        :return: instagram's username
        """
        if "instagram" in self._profile_json_format:
            return self._profile_json_format['instagram']['username']
        else:
            return None

    @property
    def instagram_photos(self):
        """Obtain instagram photos of an user.

        :return: a generator  with photos
        """
        if "instagram" in self._profile_json_format:
            return [p['image'] for p in self._profile_json_format['instagram']['photos']]
        else:
            return None

    @property
    def gender(self):
        """Obtain a gender of an user

        :return: an user's gender.
        """
        return GENDER_MAP[int(self._profile_json_format['gender'])]

    @property
    def common_likes(self):
        """Common likes.

        :return: a generator with common likes
        """
        return [p for p in self._profile_json_format['common_likes']]

    @property
    def common_connections(self):
        """Common connections.

        :return: a generator with common connections
        """
        return [p for p in self._profile_json_format['common_connections']]

    @property
    def thumbnails(self):
        """Obtain 84x84 photos

        :return: photos of an user with 84x84 resolution.
        """
        return self.get_photos(width=84)

    @property
    def photos(self):
        """Get all photos of an user.

        :return: a generator with Tinder's photos.
        """
        return self.get_photos()

    @property
    def distance_km(self):
        """Get distance in kilometers.

        :return: a distance in kilometers.
        """
        if 'distance_km' in self._profile_json_format:
            return self._profile_json_format['distance_km']
        elif 'distance_mi' in self._profile_json_format:
            return self._profile_json_format['distance_mi'] * 1.60934
        else:
            return -1

    @property
    def distance_mi(self):
        """Get distance in miles.

        :return: a distance in miles.
        """
        if 'distance_mi' in self._profile_json_format:
            return self._profile_json_format['distance_mi']
        elif 'distance_km' in self._profile_json_format:
            return self._profile_json_format['distance_km'] / 1.60934
        else:
            return -1

    @property
    def age(self):
        """Get age.

        :return: age of an user.
        """
        today = datetime.date.today()
        return (today.year - self.birth_date.year -
                ((today.month, today.day) <
                 (self.birth_date.month, self.birth_date.day)))

    def get_photos(self, width=640):
        """Get photos of an user.
        The base size is 640x640 (max size)

        :param width: the width of obtained image. It has to be in {84, 172, 320, 640} (640 by default)
        :return: photo's generator.
        """
        if int(width) not in VALID_PHOTO_SIZES:
            raise ValueError("Unsupported width")
        return itertools.chain.from_iterable(
            [
                [
                    processed_photo['url'] for processed_photo in
                    photo.get("processedFiles", []) if
                    processed_photo['width'] == int(width)
                ] for photo in self._photos
            ]
        )

    @property
    def share_link(self):
        """Share link.

        :return: the shared link
        """
        return self._session._api.share(self.id)['link']

    def __unicode__(self):
        return u"{n} ({a})".format(n=self.name, a=self.age)

    def __str__(self):
        return six.text_type(self).encode('utf-8')

    def __repr__(self):
        return repr(self.name)

    def report(self, cause, text=""):
        """Report an user.

        :param cause: the cause of a report
        :param text: the body of a report ("" by default)
        :return: response
        """
        return self._session._api.report(self.id, cause, text)

    def like(self):
        """Like an user and obtain if match.

        :return: is an user match
        """
        return self._session._api.like(self.id)['match']

    def superlike(self):
        """Superlike an user and obtain if match.

        :return: is an user match
        """
        return self._session._api.superlike(self.id)['match']

    def dislike(self):
        """Dislike an user and obtain if match.

        :return: response
        """
        return self._session._api.dislike(self.id)


class RateLimited(User):
    pass


class Match:
    """The class which define a match and send a message to the matched user
    """
    def __init__(self, match, _session):
        """Define a match.

        :param match: the json profile of a matched user
        :param _session: a session
        """
        self._session = _session
        self.id = match["_id"]
        self.user, self.messages = None, []
        self.match_date = datetime.datetime.strptime(match["created_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if 'person' in match:
            user_data = _session._api.user_info(match['person']['_id'])['results']
            user_data['_id'] = match['person']['_id']
            self.user = User(user_data, _session)
            self.messages = [Message(mes, user=self.user) for mes in match['messages']]

    def message(self, body):
        """Send message

        :param body: the body of a message.
        :return: user's id
        """
        return self._session._api.message(self.id, body)['_id']

    def message_gif(self, giphy_id):
        """Send a gif message.

        :param giphy_id: id of a gif.
        :return: user's id
        """
        return self._session._api.message_gif(self.id, giphy_id)['_id']

    def report(self, cause, text=""):
        """Report an user.

        :param cause: cause of a report
        :param text: body of report ("" by default)
        :return: response
        """
        return self._session._api.report(self.id, cause, text)

    def delete(self):
        """Unmatch an user.

        :return: response
        """
        return self._session._api._delete('/user/matches/' + self.id)

    def __repr__(self):
        return "<Unnamed match>" if self.user is None else repr(self.user)
