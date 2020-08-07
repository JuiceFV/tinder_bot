"""The basic global variables for tinder's Api.
"""
from enum import Enum

# Host of the tinder API
HOST = 'https://api.gotinder.com'
# Content's host of the tinder
CONTENT_HOST = 'https://content.gotinder.com'

# endpoints which are adds up to the base link ('https://content.gotinder.com'/'https://api.gotinder.com')
KEY_ENDPOINTS = {
    'fb_auth': {'method': 'POST', 'endpoint': '/v2/auth/login/facebook'},
    'recs': {'method': 'POST', 'endpoint': '/user/recs'},
    'profile': {'method': 'POST', 'endpoint': '/profile'},
    'updates': {'method': 'POST', 'endpoint': '/updates'},
    'meta': {'method': 'GET', 'endpoint': '/meta'}
}

# headers passes along with a request
HEADERS = {
    'host': 'api.gotinder.com',
    'x-client-version': '47217',
    'app-version': '467',
    'Proxy-Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-GB;q=1, fr-FR;q=0.9',
    'platform': 'ios',
    'Content-Type': 'application/json',
    'User-Agent': 'Tinder/11.18.0 (iPhone; iOS 12.4.7; Scale/2.00)',
    'Connection': 'keep-alive',
    'os_version': '90000200001'
}

# https://en.wikipedia.org/wiki/User_agent
USER_AGENT = 'Tinder/11.18.0 (iPhone; iOS 12.4.7; Scale/2.00)'

# authorization through the facebook
FB_AUTH_LINK = 'https://www.facebook.com/v7.0/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd'

# Gender's map
GENDER_MAP = ("male", "female")

# Photo's valid sizes
VALID_PHOTO_SIZES = {84, 172, 320, 640}

# Gender's reverse map
GENDER_MAP_REVERSE = {"male": 0, "female": 1}

# Fields which you can update through the code
UPDATABLE_FIELDS = [
    'gender', 'age_filter_min', 'age_filter_max',
    'distance_filter', 'bio', 'interested_in',
    'discoverable'
]


class ReportCause(Enum):
    """Report causes class
    """
    Other = 0
    Spam = 1
    Inappropriate_Photos = 4
    Bad_Offline_Behavior = 5
    Inappropriate_Messages = 6
