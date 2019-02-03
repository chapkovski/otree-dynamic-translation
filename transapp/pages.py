from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

# =====================================================================================================================
# For the following three classes the explanation is provided in Readme.
class TransMixin:
    def get_context_data(self, **context):
        user_language = self.session.config.get('language', 'en')
        translation.activate(user_language)
        return super().get_context_data(**context)


class Page(TransMixin, Page):
    pass


class WaitPage(TransMixin, WaitPage):
    pass

# =====================================================================================================================
# 'Normal pages' begin ================================================================================================

class MyPage(Page):
    form_model = 'player'
    form_fields = ['age', 'mood']

    def vars_for_template(self):
        return {'myvar': _('myvarvalue')}


class ResultsWaitPage(WaitPage):
    body_text = _('You should wait')
    title_text = _('Be patient!')

    def after_all_players_arrive(self):
        pass


class Results(Page):
    def vars_for_template(self):
        # if something was already marked for translation (as in MyPage class above) you don't need to
        # mark it again, you can just put this variable into {% trans %} tag on a template.
        return {'myvar': ('myvarvalue')}


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
