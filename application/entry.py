"""The entry point for the entire bot.
"""
import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from skimage.io import imread
from time import sleep
from random import randint
from application.sources.image_processing import extract_faces
import numpy as np
from keras.models import load_model
import application.sources.pytinder as pytinder
from application.sources.config_handler import upload_config
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="Tinder-Bot user's validator")
parser.add_argument(
                    '-c',
                    '--config',
                    type=argparse.FileType('r'),
                    help="Path to configuration file"
                    )
parser.add_argument(
                    '-s',
                    '--show',
                    help="Whether you wish to see girl's photos or not: 1 - yes, you do 0 - no, you don't",
                    default=1,
                    )
args = parser.parse_args()

index = 0


def obtain_data_for_prediction(user, compiled_model):
    """This function obtains all required data for a prediction.
    Due to the bot scrolling through the all photos and estimate likelihood for every single one in purpose
    to measure expectation value and compare it with mean value.

    :param user: user's object
    :param compiled_model: compiled CNN model

    :return probability_set: the set of probability for each photo
    :return photos_set: tensor of np-array's photos
    :return n: number of successfully retrieved photos
    """
    probability_set = []
    photos_set = []
    n = 0
    photos = user.get_photos()
    for photo in photos:
        face = np.array(extract_faces(imread(photo)))
        if len(face) != 0:
            prediction = compiled_model.predict(face)
            n += 1
            probability_set.append(prediction[0][1])
            photos_set.append(imread(photo))
    if n != 0:
        return probability_set, photos_set, n
    else:
        return None, None, None


def estimate_expectation(prob_set):
    """Estimates expectation value.

    :param prob_set: probability set for E[x] estimation.
    :return expectation: Measured value.
    """
    expectation = 0
    for probability in prob_set:
        expectation += probability
    return expectation


def _canvas(photos_set, probability_set, width=12, height=6):
    """The function represents photos of a girl before each bot's decision

    :param photos_set: set of representing photos
    :probability set: probability of like/dislike for each photo
    :param width: width of a canvas
    :param height: height of a canvas
    """
    fig = plt.figure(figsize=(width, height))
    len_of_images = len(photos_set)
    global index

    def scroll_function(event):
        """The very scroll function.

        :param event: if an user performs an action using mouse's wheel. Event contains details.
        """
        global index

        # If the button is up then scrolling to the next photo. If an user currently at last photo then we go from
        # the head again.
        if event.button == 'up':
            if index == len_of_images - 1:
                index = 0
            else:
                index += 1
        # If the button is down then scrolling to the previous photo. If an user currently at first photo then
        # we go from tail.
        elif event.button == 'down':
            if index == 0:
                index = len_of_images - 1
            else:
                index -= 1

        # show a photo and represent its position
        plt.imshow(photos_set[index])
        plt.title("{}/{} Probability you liked this photo is: {:.2f}%".format(
            (index + 1),
            len_of_images,
            probability_set[index] * 100
        ))
        plt.show()

    fig.canvas.mpl_connect('scroll_event', scroll_function)
    plt.imshow(photos_set[0])
    plt.title("{}/{} Probability you liked this photo is: {:.2f}%".format(
        (index + 1),
        len_of_images,
        probability_set[0] * 100
    ))
    plt.show()
    index = 0


def like_or_nope(user, compiled_model):
    """This function estimates E[x] and compares it with mean (n/2).

    :param user: user's object
    :param compiled_model: pre-compiled CNN model

    :return: decision like nor dislike or None if photo hasn't been retrieved
    """
    probability_set, photos_set, n = obtain_data_for_prediction(user, compiled_model)
    if n is not None:
        if args.show == 1:
            _canvas(photos_set, probability_set)
        expectation = estimate_expectation(probability_set)
        print("\nExpectation is {} or probability that you liked this profile is {:.2f}%\n".format(expectation, expectation/n * 100))
        if expectation > (n/2):
            return 'like'
        else:
            return 'dislike'
    else:
        return None


def swipe(_session, compiled_model):
    """The swap-function swapping a girl according to decision.

    :param _session: tinder's session
    :param compiled_model: pre-compiled CNN model
    """
    while True:
        users = _session.nearby_users()

        for user in users:
            action = like_or_nope(user, compiled_model)
            if action == 'like':
                user.like()
                print('The Bot liked "' + user.name + '"')
                print('-------------------------------------------------------')
                sleep(randint(3, 15))
            elif action == 'dislike':
                user.dislike()
                print('The Bot disliked "' + user.name + '"')
                print('-------------------------------------------------------')
                sleep(randint(3, 15))
            else:
                print("No photo has been obtained")


if __name__ == '__main__':
    cfg = upload_config(args.config)
    session = pytinder.Session(config=cfg['session'])
    model = load_model(cfg['model']['path'])
    swipe(session, model)
