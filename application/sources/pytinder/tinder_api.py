"""This file contains the wrapper for tinder API. The most of code has been copied from pynder package
(https://github.com/charliewolf/pynder.) However I've enhanced this package by adding the proper facebook authorization.
Also I've adapted pynder for my own purposes by getting rid of some redundant (to me of course) methods.
"""
import requests
import json
import threading
from application.sources.pytinder import globals
from application.sources.pytinder.utilits import get_facebook_access_token
import application.sources.pytinder.exceptions as errors

__all__ = ('TinderAPI',)


class TinderAPI:
    """The base API class, methods of this class interacts with tinder API
    """

    def __init__(self, x_auth_token=None):
        """
        The constructor of the TinderAPI class, it is initializing a session.
        :param x_auth_token: if an user somehow retrieved XAuthToken, he could pass it. (None by default)
        """
        self._session = requests.Session()
        self._session.headers.update(globals.HEADERS)
        self._x_auth_token = x_auth_token

        # If an user passed a XAuthToken it should be updated in headers dict.
        if self._x_auth_token:
            self._session.headers.update({'Authorization': "Token token='#{'" + str(self._x_auth_token) + "'}'"})
            self._session.headers.update({'X-Auth-Token': str(self._x_auth_token)})

    @staticmethod
    def _tie_link(end_point):
        """The method which helps to create proper URL.

        :param end_point: the endpoint of a requested link.
        :return: built up link
        """
        _url = end_point.lower()

        # In case if passes entire link then returns itself
        if _url.startswith("http://") or _url.startswith("https://"):
            return end_point
        # However if passes endpoint then builds integral link and returns it.
        else:
            return globals.HOST + end_point

    def _get_xauth_token(self, fb_auth_token):
        """In most of case use this method to retrieve a XAuthToken.

        :param fb_auth_token: the authentication token obtained from facebook using your fb email and fb password.
        :return: either a token nor None if token is missing.
        """
        response = self._session.request(
            globals.KEY_ENDPOINTS['fb_auth']['method'],
            globals.HOST + globals.KEY_ENDPOINTS['fb_auth']['endpoint'],
            headers={'app_version': '11', 'platform': 'ios', 'content-type': 'application/json'},
            data=json.dumps({'token': fb_auth_token}),
            timeout=1,
        )
        if response.status_code == 200:
            return response.json()['data']['api_token']
        else:
            return None

    def auth(self, facebook_email, facebook_password):
        """Method performs authentication an user in tinder.

        :param facebook_email: user's facebook email
        :param facebook_password: user's facebook password
        """
        if self._x_auth_token is None:
            # If a XAuthToken hasn't passed, yet I retrieve a token using fb password and fb email.
            self._x_auth_token = self._get_xauth_token(get_facebook_access_token(facebook_email, facebook_password))
            if self._x_auth_token is None:
                raise errors.InitializationError("Authorization has been wrong. Couldn't retrieve a tinder's token.\n"
                                                 "Check if your facebook's email and password are precise.")
            self._session.headers.update({'Authorization': "Token token='#{'" + str(self._x_auth_token) + "'}'"})
            self._session.headers.update({'X-Auth-Token': str(self._x_auth_token)})

    def _request(self, method, end_point, data=None):
        """Basically this method is the wrapper for any request.

        :param method: the method of a request (GET, POST, DELETE, UPDATE)
        :param end_point: the endpoint all endpoints are presented here https://github.com/fbessez/Tinder
        :param data: possible request data. (dict() by default)
        :return: response in json format
        """
        if self._x_auth_token is None:
            raise errors.InitializationError
        response = self._session.request(method, self._tie_link(end_point), data=data)
        while response.status_code == 429:
            blocker = threading.Event()
            blocker.wait(0.1)
            response = self._session.request(method, self._tie_link(end_point), data=data)
        if response.status_code < 200 or response.status_code >= 300:
            raise errors.RequestError(response.status_code)
        if response.status_code == 201 or response.status_code == 204:
            return {}
        return response.json()

    def _get(self, url):
        """Wrapper for get request

        :param url: a requested link
        :return: response
        """
        return self._request("get", url)

    def _post(self, url, data=None):
        """Wrapper for post request

        :param url: a requested link
        :param data: possible request data. (dict() by default)
        :return: response
        """
        return self._request("post", url, data=data)

    def _delete(self, url):
        """Wrapper for delete request

        :param url: a requested link
        :return: response"""
        return self._request("delete", url)

    def recs(self, limit=10):
        """Request for stack of girls or boys, depends in you.

        :param limit: limit for request
        :return: response
        """
        return self._post(globals.KEY_ENDPOINTS['recs']['endpoint'], data={'limit': limit})

    def profile(self):
        """Get my/your user's profile

        :return: response
        """
        return self._get(globals.KEY_ENDPOINTS['profile']['endpoint'])

    def updates(self, since):
        """Last updates since <since>.

        :param since: date when to look for updates
        :return: response
        """
        return self._post(globals.KEY_ENDPOINTS['updates']['endpoint'], {"last_activity_date": since} if since else {})

    def meta(self):
        """Retrieve my/your own metadata. (swipes left, people seen, etc..)

        :return: response
        """
        return self._get(globals.KEY_ENDPOINTS['meta']['endpoint'])

    def add_profile_photo(self, facebook_id, x_dist, y_dist, x_offset, y_offset):
        """Adds a profile's photo to our Tinder profile.

        :param facebook_id: your facebook id.
        :param x_dist: x-axis distance (percent)
        :param y_dist: y-axis distance (percent)
        :param x_offset: x-axis offset (percent)
        :param y_offset: y-axis offset (percent)
        """
        data = {
            "transmit": "fb",
            "assets": [
                {
                    "id": str(facebook_id),
                    "xdistance_percent": float(x_dist),
                    "ydistance_percent": float(y_dist),
                    "xoffset_percent": float(x_offset),
                    "yoffset_percent": float(y_offset)
                }
            ]
        }

        return self._request("post", globals.CONTENT_HOST + globals.KEY_ENDPOINTS['meta']['endpoint'], data=data)

    def delete_profile_photo(self, photo_id):
        """Delete profile photo from Tinder profile.

        :param photo_id: id of deleting photo.
        :return: response
        """
        data = {"assets": [photo_id]}

        return self._request("delete", globals.CONTENT_HOST + globals.KEY_ENDPOINTS['meta']['endpoint'], data=data)

    def matches(self, since):
        """Check how many matches you have.

        :param since: Search for the updates since to
        :return: found matches
        """
        return self.updates(since)['matches']

    def update_profile(self, profile):
        """Update your profile.

        :param profile: updated profile
        :return: response
        """
        return self._post(globals.KEY_ENDPOINTS['profile']['endpoint'], profile)

    def like(self, user):
        """Like an user.

        :param user: user which to like
        :return: response
        """
        return self._get(f"/like/{user}")

    def dislike(self, user):
        """Dislike an profile.

        :param user: user which to like
        :return: response
        """
        return self._get(f"/pass/{user}")

    def message(self, user, body):
        """Message to an user.

        :param user: an user to message to
        :param body: the body of a message
        :return: response
        """
        return self._post(f"/user/matches/{user}", {"message": str(body)})

    def message_gif(self, user, giphy_id):
        """Message to an user with a gif.

        :param user: an user to message to
        :param giphy_id: the id of a gif
        :return: response
        """
        return self._post(f"/user/matches/{user}", {"type": "gif", "gif_id": str(giphy_id)})

    def report(self, user, cause=globals.ReportCause.Other, text=""):
        """Report an user.

        :param user: an user to message to
        :param cause: the class of report's causes:
        Other/Spam/Inappropriate_Photos/Bad_Offline_Behavior/Inappropriate_Messages
        (Other by default)
        :param text: the additional message to a report. ("" by default)
        :return: response
        """
        try:
            cause = int(cause)
        except TypeError:
            cause = int(cause.value)

        data = {"cause": cause}

        if text and globals.ReportCause(cause) == globals.ReportCause.Other:
            data["text"] = text

        return self._post("/report/" + user, data)

    def user_info(self, user_id):
        """Obtain all information about an user

        :param user_id: an user's id
        :return: response
        """
        return self._get("/user/" + user_id)

    def ping(self, lat, lon):
        """Particularly update a profile's location

        :param lat: latitude
        :param lon: longitude
        :return: response
        """
        return self._post("/user/ping", {"lat": lat, "lon": lon})

    def share(self, user):
        """Share an user profile.

        :param user: an user
        :return: response
        """
        return self._post(f"/user/{user}/share")

    def superlike(self, user):
        """Superlike an user.

        :param user: an user
        :return: response
        """
        result = self._post(f"/like/{user}/super")
        if 'limit_exceeded' in result and result['limit_exceeded']:
            raise errors.RequestError("Superlike limit exceeded")
        return result

    def fb_friends(self):
        """Requests records of all facebook friends using Tinder Social.

        :return: object containing array of all friends who use Tinder Social.
        """
        return self._get("/group/friends")

    def like_message(self, message):
        """Hearts a message sent by a match

        :param message: message id
        :return: empty json, response code is 201 (Created)
        """
        return self._post(f"/message/{message.id}/like")

    def unlike_message(self, message):
        """Removes heart from a message

        :param message: message id
        :return: empty json, response code is 204 (No content)
        """
        return self._delete(f"/message/{message.id}/like")

    def liked_messages(self, since):
        """Obtain liked message.

        :return: liked messages
        """
        return self.updates(since)['liked_messages']
