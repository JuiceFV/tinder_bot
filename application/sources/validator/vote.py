"""This module contains the class responsible for voting for a girl.
"""

import application.sources.validator.exception as errors
from matplotlib.widgets import CheckButtons
import matplotlib.pyplot as plt


class Vote:
    """The class itself sets n boxes to a plot with image.
    Each posses two choice's buttons (Like/Dislike).
    You can select the only one for every box.
    """
    def __init__(self, labels, axes_data):
        """Constructor. Initialize everything, some explanations follow below.

        :param labels: list of labels of check buttons ['Like', 'Dislike']
        :param axes_data: list of dictionaries, which in its turn contains data for checkboxes, specifically an owner's
        name and position of its box. Ex: [{'name': name1, 'rect': [1,1,1,1]}{'name': name2, 'rect': [2,2,2,2]}].
        """
        if len(axes_data) == 0:
            raise errors.VoteDefinition("Passed empty axes")

        if len(labels) == 0:
            raise errors.VoteDefinition("Passed empty labels")

        # Raise the exception if in any of passed box missing either name or rect.
        for box_data in axes_data:
            if not ('name' in box_data and 'rect' in box_data):
                raise errors.VoteDefinition("Missing some field of axes_data.")

        # Will fill further
        self._names = []
        # Labels (['Like', 'Dislike'])
        self._labels = labels
        # Decisions of participants {'name1': Decision, 'name2': Decision, ...}
        self._decisions = {}
        for person in axes_data:
            # Set axes of checkbox of a person. self.ax_name1, self.ax_name2, ...
            setattr(self, 'ax_' + person['name'], plt.axes(person['rect']))
            self._names.append(person['name'])
            self._decisions.update({person['name']: ''})
            # set buttons, self.name1_check = CheckButtons(self.ax_name1, self._labels))
            setattr(self, person['name'] + '_check', CheckButtons(getattr(self, 'ax_' + person['name']), self._labels))
            # set on click action for each button.
            getattr(self, person['name'] + '_check').on_clicked(
                lambda label, name=person['name']: self._checkbox_onclick_factory(label, name)
            )

    def set_invisible(self):
        """The function hides all boxes.
        """
        for name in self._names:
            getattr(self, 'ax_' + name).remove()

    def _checkbox_onclick_factory(self, label, name):
        """This method responsible for reciprocity to buttons.

        :param label: Chosen label (Like/Dislike)
        :param name: name of a box "owner"
        """
        reverse_states = [1, 0]
        # retrieving owner's check buttons
        check_box = getattr(self, name + '_check')
        # and obtain their status [True/False, True/False]
        buttons_state = check_box.get_status()
        # if two buttons were picked then set the last chosen as active.
        if buttons_state == [True, True]:
            check_box.set_active(reverse_states[self._labels.index(label)])

        # tie user's decision with his name for further usage
        self._decisions[name] = label

        # In the case if user hasn't chose an option set his decision as empty.
        if buttons_state == [False, False]:
            self._decisions[name] = ''

    @property
    def get_decisions(self):
        """Return the dictionary pf user's decisions.

        :return: If at least one checkbox is empty (w/o chosen option) return None to handle it as error further.
        If all is fine then return dict of decisions.
        """
        for name in self._names:
            if self._decisions[name] == '':
                return None
        return self._decisions

    @property
    def get_vote_axes(self):
        """Returns the vote axes in purpose to convey control in plot to vote.

        :return: vote axes.
        """
        return getattr(self, 'ax_' + self._names[0])

