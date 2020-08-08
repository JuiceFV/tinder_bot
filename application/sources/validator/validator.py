"""The module contains the class responsible for image's validation.
"""
from application.sources.pytinder import Session
from application.sources.validator.represent import Canvas
from path import Path


class Validator:
    """The class represent girl's photos to you. And allows to like/dislike them.
    """
    def __init__(self, config):
        """The constructor initialize a validator.
        """
        # a session which links us to tinder
        self._session = Session(config=config['session'])
        # sometimes profiles repeat, add them up to dictionary
        self._id_showed_profiles = {}

        self._canvas_data = config['canvas']

        # I don't wish ever see the repeated profiles, therefore add them up to the file.
        self._path_to_file = Path(__file__).parent.parent.parent.parent / config['seen_profiles']['filename']
        file = open(self._path_to_file, 'r')
        # And upload them at the beginning of the program.
        for line in file:
            self._id_showed_profiles.update({line[0:-1]: 1})

    @property
    def _list_of_users(self):
        """Returns a generator to a nearby user.

        :return: generator of found users
        """
        return self._session.nearby_users()

    def start(self):
        """Showing a girl.
        """
        for user in self._list_of_users:
            if user.id not in self._id_showed_profiles:
                self._id_showed_profiles.update({user.id: 1})
                file = open(self._path_to_file, 'a')
                file.write(user.id + '\n')
                print(f"user id: {user.id}\nName: {user.name}\nAge: {user.age}")
                canvas = Canvas(
                    self._canvas_data['judges'],
                    width=self._canvas_data['size']['width'],
                    height=self._canvas_data['size']['height'],
                    images_gen=user.photos
                )
                canvas.show()
