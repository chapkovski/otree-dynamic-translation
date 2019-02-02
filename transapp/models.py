from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.utils.translation import gettext as _

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'transapp'
    players_per_group = None
    num_rounds = 1
    translated_languages = ['en','ru']

TRNSL_ERR_MSG = 'Translation for this language does not exist'


class Subsession(BaseSubsession):
    def creating_session(self):
        assert self.session.config.get('language', 'en') in Constants.translated_languages, TRNSL_ERR_MSG


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    something = models.StringField(initial=_('smth dfrnt'))
