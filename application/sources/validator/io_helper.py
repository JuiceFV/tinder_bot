"""The module contains the only function which saves images to an appropriate directory.
"""

from path import Path
import requests
from PIL import Image


def url_to_image(url):
    """Auxiliary function retrieves photos from URL.

    :param url: photo URL
    :return: float image.
    """
    image = Image.open(requests.get(url, stream=True).raw)
    return image


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
    # Removes the rest after '.<extension>'
    image_name = image_name.split("?")[0]
    # Get the part with extension and unique name
    image_name = image_name.split("/")[-1]
    # Get rid of the size if it exists
    image_name = image_name.split("_")[-1]
    # Get rid of extension (in case .webp it's crucial)
    file_url_list = image_name.split(".")[0]
    filename += (file_url_list + '.jpg')
    print(filename)
    image.save(filename)
    return True

