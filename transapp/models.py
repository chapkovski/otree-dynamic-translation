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
    translated_languages = ['en', 'ru']
    example_constant = _('WAT?!')


TRNSL_ERR_MSG = 'Translation for this language does not exist'

class Subsession(BaseSubsession):
    def creating_session(self):
        assert self.session.config.get('language', 'en') \
               in Constants.translated_languages, TRNSL_ERR_MSG


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label=_('How old are you?'), help_text=_('Enter any number more than 0'),
                              )
    mood = models.IntegerField(choices=[(0, _('Good')), (1, _('Bad'))],
                               label=_('Mood'),
                               help_text=_(f'{Constants.example_constant}Your mood today?'),
                               widget=widgets.RadioSelectHorizontal)

    @property
    def get_other(self):
        return self.get_others_in_group()[0]
