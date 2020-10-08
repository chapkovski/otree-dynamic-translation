from otree.api import Currency as c, currency_range
from ._builtin import Page as oTreePage, WaitPage
from .models import Constants
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



class Page( oTreePage):
    def get_context_data(self, **context):
        user_language = self.request.GET.get('language')
        if user_language:
            translation.activate(user_language)
            if hasattr(settings, 'LANGUAGE_SESSION_KEY'):
                self.request.session[settings.LANGUAGE_SESSION_KEY] = user_language
        return super().get_context_data(**context)





