"""The module represents the class responsible for entire canvas.
Canvas has to incorporate a list of girl's photos and checkboxes for voting.
"""
import matplotlib.pyplot as plt
from application.sources.validator.io_helper import url_to_image
import application.sources.validator.exception as errors
from application.sources.validator.vote import Vote
from application.sources.validator.io_helper import save_image

class Canvas:
    """The class allows us to represent girl's photos and scroll among them.
    Also, it admits to vote for a girl.
    """
    def __init__(self, judges_data, width=12, height=6, image_links_stack=None, images_gen=None):
        """The constructor.
        :param judges_data: the list which represents data regard judges, specifically labels (Like/Dislike) and
        checkboxes data.
        :param width: the width of a canvas (figure)
        :param height: the height of a canvas (figure)
        :param image_links_stack: a list of image's (photo's) urls
        :param images_gen: image generator, which we retrieve from nearby_users()
        """
        self._judges = judges_data
        # The very figure
        self._fig = plt.figure(figsize=(width, height))
        # The links (which are links to these images)
        self._images_names = []
        # The image's list, images derived from images_gen stores over here
        self._images_stack = []
        # Index of current photo. (I've made the ability of scrolling through images)
        self._index = 0
        # Current axes (images' axes)
        self._ax = None
        # The vote object
        self._vote = None
        # Depict if the scrolling mode is on.
        self._scrolling_mode = True
        self._boxes_data = [
            {
                'name': judges_data['names'][i],
                'rect': judges_data['boxes_pos'][judges_data['names'][i]]
            } for i in range(len(judges_data['names']))
        ]

        # Check if whether image_links_stack or images_gen is passed
        if not image_links_stack and not images_gen:
            raise errors.UndefinedBehaviorOfImageDefinition("You should pass at least one of image_links_stack or "
                                                            "image_links_stack.")

        # Check if the only item is passed.
        if image_links_stack and images_gen:
            raise errors.UndefinedBehaviorOfImageDefinition("You passed both photos generator and photos links.")

        # If a user passes image_links_stack then filling self._images_names and self._images_stack
        # via image_links_stack
        if image_links_stack:
            for image in image_links_stack:
                self._images_names.append(image)
                self._images_stack.append(url_to_image(image))

        # If a user passes images_gen then filling self._images_names and self._images_stack via images_gen
        if images_gen:
            for image in images_gen:
                self._images_names.append(image)
                self._images_stack.append(url_to_image(image))

        # Store a number of photos for representation while scrolling.
        self._len_of_images = len(self._images_stack)
        plt.title(f"{self._index + 1}/{self._len_of_images}")

    def _scroll_factory(self):
        """The factory, which allows an user to scroll through images using mouse's wheel.
        """
        def scroll_function(event):
            """The very scroll function.

            :param event: if an user performs an action using mouse's wheel. Event contains details.
            """
            # If the button is up then scrolling to the next photo. If an user currently at last photo then we go from
            # the head again.
            if event.button == 'up':
                if self._index == self._len_of_images - 1:
                    self._index = 0
                else:
                    self._index += 1
            # If the button is down then scrolling to the previous photo. If an user currently at first photo then
            # we go from tail.
            elif event.button == 'down':
                if self._index == 0:
                    self._index = self._len_of_images - 1
                else:
                    self._index -= 1

            # show a photo and represent its position
            plt.imshow(self._images_stack[self._index])
            plt.title(f"{self._index + 1}/{self._len_of_images}")
            plt.show()

        # connect the function to the wheel
        self._scroll_id = self._fig.canvas.mpl_connect('scroll_event', scroll_function)
        return scroll_function

    def _click_factory(self):
        """The factory which implements the behavior of mouse's click and keyboard buttons.
        """
        def click_function(event):
            """The function which handles mouse clicks.
            """
            # If mouse wheel is pressed and scrolling mode is on (if we already in vote mode it shouldn't works)
            if event.button == 2 and self._scrolling_mode:
                def submit_check(e):
                    """The function which submit a vote.
                    """
                    # If the Enter has been pressed then we making an effort to save in image to a file
                    # (move to a directory)
                    if e.key == 'enter':
                        saved = save_image(
                            self._images_stack[self._index],
                            self._images_names[self._index],
                            self._vote.get_decisions
                        )

                        # If an image is saved then turn back to girl's images. Otherwise print that voting went wrong.
                        if saved:
                            # Remove vote's boxes
                            self._vote.set_invisible()
                            # Turn the scrolling mode on
                            self._scrolling_mode = True
                            # Disconnect submit function from enter button
                            self._fig.canvas.mpl_disconnect(self._submit_id)
                            # Reconnect the scroll function which has been disconnected (disconnection is below).
                            self._scroll_factory()
                            # Reset axes to images.
                            plt.sca(self._ax)
                            plt.show()
                        else:
                            print("Wrong vote.\n")

                # I'd like to recall we still in voting mode (pressed mouse's wheel).
                # Turn scrolling mode off
                self._scrolling_mode = False
                # Disconnect scrolling function (after this step mouse's wheel scrolling doesn't work)
                self._fig.canvas.mpl_disconnect(self._scroll_id)
                # Connect the submit function, it allows us to check the votes by Enter pressing.
                self._submit_id = self._fig.canvas.mpl_connect('key_press_event', submit_check)
                # Create a vote. It admits Labels and Checkbox's axes data
                # Note: that Checkbox's axes data passes in the order as your folder's names arranged.
                # For instance I have the folders like <milka-yes_sabbatini_no_me-yes_> and like that, consequently
                # I have to arrange the list of dictionaries in the names' order.
                self._vote = Vote(
                    self._judges['labels'],
                    self._boxes_data
                )
                # Set checkboxes as the main axes.
                plt.sca(self._vote.get_vote_axes)
                plt.show()

            # However, if the right button is clicked and we're in voting mode then turn it off.
            elif event.button == 3 and not self._scrolling_mode:
                # Turn the scrolling mode on
                self._scrolling_mode = True
                # Remove vote's boxes
                self._vote.set_invisible()
                # Disconnect submit function from enter button
                self._fig.canvas.mpl_disconnect(self._submit_id)
                # Reconnect the scroll function which has been disconnected (disconnection is below).
                self._scroll_factory()
                # Reset axes to images.
                plt.sca(self._ax)
                plt.show()

        # Connect click function to a canvas
        self._fig.canvas.mpl_connect('button_press_event', click_function)
        return click_function

    def add_images(self, images_gen=None, image_links_stack=None):
        """The function adds images to the stack.

        :param image_links_stack: a list of image's (photo's) urls
        :param images_gen: image generator, which we retrieve from nearby_users()
        """

        # Check if whether image_links_stack or images_gen is passed
        if not image_links_stack and not images_gen:
            raise errors.UndefinedBehaviorOfImageDefinition("You should pass at least on of image_links_stack or "
                                                            "image_links_stack.")

        # Check if the only item is passed.
        if image_links_stack and images_gen:
            raise errors.UndefinedBehaviorOfImageDefinition("You passed both photos generator and photos links.")

        # If a user passes image_links_stack then filling self._images_names and self._images_stack
        # via image_links_stack
        if image_links_stack:
            for image in image_links_stack:
                self._images_names.append(image)
                self._images_stack.append(url_to_image(image))

        # If a user passes images_gen then filling self._images_names and self._images_stack via images_gen
        if images_gen:
            for image in images_gen:
                self._images_names.append(image)
                self._images_stack.append(url_to_image(image))

    @property
    def images_links(self):
        """Returns a list of image's names (URLs).

        :return: images name
        """
        return self._images_names

    @property
    def images_as_np_array(self):
        """Returns a list of images.

        :return: images stack
        """
        return self._images_stack

    @staticmethod
    def _close_plot_key_event(event):
        """The function which close a canvas if control is pressed.
        """
        if event.key == 'control':
            plt.close()

    def show(self):
        """Show a canvas.
        """
        if not self._images_stack:
            raise errors.ImagesNotFound("Images are not defined")
        # Connect close function to a canvas.
        self._fig.canvas.mpl_connect('key_press_event', self._close_plot_key_event)
        # Connect scroll function
        self._scroll_factory()
        # Connect click function
        self._click_factory()
        plt.imshow(self._images_stack[0])
        self._ax = self._fig.axes[0]
        plt.show()
