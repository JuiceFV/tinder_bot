"""The module contains the only function which saves images to an appropriate directory.
"""

from skimage.io import imsave
from path import Path


def save_image(image, image_name, decisions):
    """The function which save an image in a proper place.

    :param image: the image to save.
    :param image_name: the image's name which will be saved.
    :param decisions: the dictionary of each voter's decision.
    :return: True/False depends on if an image is saved.
    """
    filename = Path(__file__).parent.parent.parent.parent / 'samples/'
    if decisions is None:
        return False
    for name in decisions:
        filename += name
        if decisions[name] == 'Like':
            filename += '-yes_'
        elif decisions[name] == 'Dislike':
            filename += '-no_'

    filename += '/'
    file_url_list = image_name.split("/")
    filename += file_url_list[-1]
    print(filename)
    imsave(filename, image)
    return True

