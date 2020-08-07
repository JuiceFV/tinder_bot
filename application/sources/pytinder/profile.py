"""This module contains classes responsible for your profile.
"""
import dateutil
from application.sources.pytinder.globals import GENDER_MAP, GENDER_MAP_REVERSE, UPDATABLE_FIELDS
from application.sources.pytinder.exceptions import UserInitializationError
import datetime


class ProfileDescriptor:
    """This is a python descriptor that allows for
    dynamic updating of profile data
    """

    def __init__(self, id):
        self.id = id

    def __get__(self, instance, owner):
        if hasattr(self, 'value'):
            return self.value
        else:
            try:
                return instance._profile_json_format[self.id]
            except KeyError:
                return None

    def __set__(self, instance, value):

        profile = {}
        for key in UPDATABLE_FIELDS:
            profile[key] = getattr(instance, key)
        profile['gender'] = GENDER_MAP_REVERSE[profile['gender']]
        profile['interested_in'] = [GENDER_MAP_REVERSE[x] for x in profile['interested_in']]
        profile[self.id] = value
        instance.__init__(instance._api.update_profile(profile), instance._api)
        self.value = value


class GenderDescriptor(ProfileDescriptor):
    """makes gender human readable
    """

    def __get__(self, instance, owner):
        gender = super(GenderDescriptor, self).__get__(instance, owner)
        return GENDER_MAP[gender]

    def __set__(self, instance, value):
        gender = GENDER_MAP_REVERSE[value]
        return super(GenderDescriptor, self).__get__(instance, gender)


class InterestedInDescriptor(ProfileDescriptor):
    """makes interested in human readable
    """

    def __get__(self, instance, owner):
        interested_in = super(InterestedInDescriptor, self).\
            __get__(instance, owner)
        return list(map(lambda x: GENDER_MAP[x], interested_in))

    def __set__(self, instance, value):
        interested_in = map(lambda x: GENDER_MAP_REVERSE[x], value)
        return super(InterestedInDescriptor, self).\
            __get__(instance, interested_in)


class Profile:
    bio = ProfileDescriptor('bio')
    discoverable = ProfileDescriptor('discoverable')
    distance_filter = ProfileDescriptor('distance_filter')
    age_filter_min = ProfileDescriptor('age_filter_min')
    age_filter_max = ProfileDescriptor('age_filter_max')
    interested_in = InterestedInDescriptor('interested_in')
    gender = GenderDescriptor('gender')

    def __init__(self, profile_json, api):
        try:
            self.id = profile_json['_id']
            self._api = api
            self.photos = list(map(lambda photo: str(photo['url']), profile_json['photos']))
            self.ping_time = profile_json['ping_time']
            self.name = profile_json['name']
            self.birth_date = dateutil.parser.parse(profile_json['birth_date'])
            self.create_date = dateutil.parser.parse(profile_json['create_date'])
            self.interests = profile_json['interests']
            self.jobs = []
            self.schools = []
            self.email = profile_json['email']
            self.gender_filter = profile_json['gender_filter']

            try:
                self.pos = profile_json['pos']
            except KeyError:
                self.pos = None

            try:
                self.schools.extend(["%s" % school["name"] for school in profile_json['schools'] if 'name' in school])
                self.jobs.extend(["%s @ %s" % (job["title"]["name"], job["company"]["name"]) for job in profile_json['jobs'] if 'title' in job and 'company' in job])
                self.jobs.extend(["%s" % (job["company"]["name"],) for job in profile_json['jobs'] if 'title' not in job and 'company' in job])
                self.jobs.extend(["%s" % (job["title"]["name"],) for job in profile_json['jobs'] if 'title' in job and 'company' not in job])
            except (ValueError, KeyError):
                pass

            self.banned = profile_json['banned'] if "banned" in profile_json else False
            self._profile_json_format = profile_json
        except UserInitializationError:
            print("The initialization of a user has went wrong.\nPerhaps the profile you passed is incorrect.")

    def __repr__(self):
        return self.name

    @property
    def age(self):
        today = datetime.date.today()
        return (today.year - self.birth_date.year -
                ((today.month, today.day) <
                 (self.birth_date.month, self.birth_date.day)))

    def add_photo(self, facebook_id, x_dist=1, y_dist=1, x_offset=0, y_offset=0):
        return self._api.add_profile_photo(facebook_id, x_dist, y_dist, x_offset, y_offset)

    def delete_photo(self, photo_id):
        return self._api.delete_profile_photo(photo_id)