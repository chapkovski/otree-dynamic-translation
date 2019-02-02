from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils import translation
from django.utils.translation import gettext as _


class TransMixin:
    def get_context_data(self, **context):
        user_language = self.session.config.get('language', 'en')
        translation.activate(user_language)
        return super().get_context_data(**context)


class Page(TransMixin, Page):
    pass


class WaitPage(TransMixin, WaitPage):
    pass


class MyPage(Page):
    form_model = 'player'
    form_fields = ['age', 'mood']

    def vars_for_template(self):
        return {'myparam': _('Dorow')}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
