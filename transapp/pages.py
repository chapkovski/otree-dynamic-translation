from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils import translation
from django.utils.translation import gettext as _


class CustomPage(Page):
    def get(self):
        user_language = self.session.config.get('language', 'en')
        translation.activate(user_language)
        return super().get()


class MyPage(CustomPage):

    def vars_for_template(self):
        return {'myparam': _('Dorow')}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(CustomPage):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
