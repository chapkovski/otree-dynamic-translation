from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django.utils.translation import ugettext_lazy as _

author = 'Philipp Chapkovski, HSE-Moscow, chapkovski@gmail.com'

doc = """
An example of dynamic language change based on app settings
"""


class Constants(BaseConstants):
    name_in_url = 'transapp'
    players_per_group = 2
    num_rounds = 1

    translated_languages = ['en', 'ru']  # This is the list of allowed languages for this app. Actually it makes sense
    # to move it to settings
    example_constant = _('Some constant')


TRNSL_ERR_MSG = 'Translation for this language does not exist'

class Subsession(BaseSubsession):
    def creating_session(self):
        # see more on the following lines in Readme. Just to check that an experimenter won't insert non available
        # option here
        assert self.session.config.get('language', 'en') \
               in Constants.translated_languages, TRNSL_ERR_MSG


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label=_('How old are you?'),
                              help_text=_('Enter any number more than 0'),
                              )
    # If you use translated choices for models, AND if you use dynamic switching, it is important
    # to use tuples, not simple lists (like [_('Good'), _('Bad')]), because otherwise when you switch the language
    # the allowed set of choices won't let user go further.
    mood = models.IntegerField(choices=[(0, _('Good')), (1, _('Bad'))],
                               label=_('Mood'),
                               help_text=_('What is your mood today?'),
                               )

    @property
    def get_other(self):
        return self.get_others_in_group()[0]
