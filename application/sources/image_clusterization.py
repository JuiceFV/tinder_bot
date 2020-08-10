"""This module contains functions responsible for image's "clusterization".
It means when we've accumulated required (desired) quantity of images and sorted them to
the folders like that: name1-yes_name2-no_name3-yes we need to shove all of these photos to the like/dislike - only
folders.
"""

from skimage.io import imsave, imread
from os import listdir
from os.path import isfile, join
from path import Path

# the base path where all samples are placed
base_path = Path(__file__).parent.parent.parent / 'samples/'
# path to the "like" folder
like_path = base_path + 'like/'
# path to the "dislike" folder
dislike_path = base_path + 'dislike/'


def _get_dir_list(names):
    """This function obtains a list of all "named"-directory [name1-yes_name2-no,  name1-no_name2-yes, etc]
    The list's building occurs dynamically, depending on your list of names (and its order) in config.yaml.
    The entire algorithm is described in "img" in the root directory and in the Readme.md.

    :param names: the names of judges, they have to be in the same order as they arranged in a filename.
    For example: if a file calls "name1-yes_name2-no_", therefore the name's list looks like [name1, name2]

    :return: list of compiled directories.
    """
    # Number of columns
    n = len(names)
    # Number of lines
    num_lines = 2**n
    # fill the result with '\0'
    dir_list = ['' for i in range(num_lines)]

    # In our case a name represents a column.
    for name in names:
        column_index = names.index(name)
        # The partition_index is the cue when we should to switch 0 to 1 (no to yes) and vise versa.
        partition_index = num_lines / (2**(column_index + 1))
        # yes_mode means that we add '-yes_' up to a name, otherwise add '-no_'.
        yes_mode = True
        line = 0
        while line < num_lines:
            path_part = name
            # Switch the mode to the opposite one.
            if line % partition_index == 0:
                yes_mode = not yes_mode
            # Sets a decision to a name
            if not yes_mode:
                path_part += '-no_'
            else:
                path_part += '-yes_'
            # Add a path's part (column by column) to the list
            dir_list[line] += path_part
            line += 1
    return dir_list


def classify_images_to_like_dislike(names):
    """The function copies images from so called "named" folders to like/dislike folders.

    :param names: list of judge's names.
    """
    # Obtain directories list
    dir_list = _get_dir_list(names)
    for directory in dir_list:
        # Retrieve the only decisions (yes/no) for instance name1-yes_name2-no_, decision_list = ['yes', 'no']
        decision_list = [person.split('-')[1] for person in directory.split('_')[:-1]]
        # Extract all files from a directory
        files = [f for f in listdir(base_path + directory + '/') if isfile(join(base_path + directory + '/', f))]
        num_of_files = len(files)
        # Get a coefficient multiplying by we get a number of images which we'ill be copying to the like-folder
        like_ratio = decision_list.count('yes') / len(decision_list)
        num_of_like_img = int(num_of_files * like_ratio)
        index = 0
        print(f"Copies {num_of_like_img} files from {directory} to likes and {num_of_files - num_of_like_img} to dislikes")
        # Copy images to like folder
        while index < num_of_like_img:
            image = imread(base_path + directory + '/' + files[index])
            imsave(like_path + files[index], image)
            index += 1
        index = num_of_like_img
        # Copy residuals images o dislike folder
        while index < num_of_files:
            image = imread(base_path + directory + '/' + files[index])
            imsave(dislike_path + files[index], image)
            index += 1


def classify_images_per_user(names):
    """Due to I was making the application for my specific purposes, I created this function which sort images
    per user decision.

    :param names: list of judge's names.
    """
    # Obtain directories list
    dir_list = _get_dir_list(names)
    for directory in dir_list:
        # Retrieve the only decisions (yes/no) for instance name1-yes_name2-no_, decision_list = ['yes', 'no']
        decision_list = [person.split('-')[1] for person in directory.split('_')[:-1]]
        # Extract all files from a directory
        files = [f for f in listdir(base_path + directory + '/') if isfile(join(base_path + directory + '/', f))]
        for i in range(len(decision_list)):
            # if a user liked photos in current directory then these photos to name_like directory
            if decision_list[i] == 'yes':
                for file in files:
                    image = imread(base_path + directory + '/' + file)
                    imsave(base_path + names[i] + '_like/' + file, image)
            # otherwise save photos to name_dislike directory
            elif decision_list[i] == 'no':
                for file in files:
                    image = imread(base_path + directory + '/' + file)
                    imsave(base_path + names[i] + '_dislike/' + file, image)
