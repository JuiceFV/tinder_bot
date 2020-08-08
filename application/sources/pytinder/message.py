"""The module contains the only class responsible for
message in the chat with an user. Further, I'd like to add up NLP and send a message
to an user, depends on user's description and his/her message. And to handle a message
I will need in class which handle it. And I not that this class has been copied from pynder.
"""

import dateutil.parser
from six import text_type

__all__ = ('Message', )


class Message:
    """The class has a reciprocity with each message.
    It can like/like dislike and obtain a message itself.
    """
    def __init__(self, data, user=None):
        """Constructor which initialize the data.

        :param data: json got from request to the tinder
        :param user: if message from an user than pass User-class as 'user'
        """
        # then entire data
        self._data = data
        # the id
        self.id = data['_id']
        # the time when a message has been sent
        self.sent = dateutil.parser.parse(data['sent_date'])
        # the very message
        self.body = data['message']

        # if an user passed then set a sender and a recipient
        if user:
            if data['from'] == user.id:
                self.sender = user
            if data['to'] == user.id:
                self.to = user
            if data['from'] == user._session.profile.id:
                self.sender = user._session.profile
            if data['to'] == user._session.profile.id:
                self.to = user._session.profile
            self._session = user._session

    def like(self):
        """Like a message

        :return: response
        """
        return self._session._api.like_message(self)

    def unlike(self):
        """Dislike a message

        :return: response
        """
        return self._session._api.unlike_message(self)

    @property
    def is_liked(self, since=None):
        """Check if messages is liked

        :param since: the date from when start to search. (None by default)
        :return: is message liked
        """
        for liked_message in self._session._api.liked_messages(since):
            if self.id == liked_message['message_id']:
                return liked_message['is_liked']
        return False

    def __unicode__(self):
        return self.body

    def __str__(self):
        return text_type(self).encode("utf8")

    def __repr__(self):
        return repr(self.body)
