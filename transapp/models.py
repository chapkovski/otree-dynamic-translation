from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
# from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import ugettext as _
author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'transapp'
    players_per_group = 2
    num_rounds = 1
    translated_languages = ['en', 'ru']
    translateble_constant=_('WAT?!')

TRNSL_ERR_MSG = 'Translation for this language does not exist'


class Subsession(BaseSubsession):
    def creating_session(self):
        assert self.session.config.get('language', 'en') in Constants.translated_languages, TRNSL_ERR_MSG


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label=_('How old are you?'), help_text=_('Enter any number more than 0'),
                              )
    mood = models.StringField(choices = [_('Good'), _('Bad')], label=_('Mood'), help_text=_('Your mood today?'),
                              widget=widgets.RadioSelectHorizontal)
