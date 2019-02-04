from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        yield (pages.MyPage, {'age': random.randint(0,100),
                              'mood': random.randint(0,1)})
        yield (pages.Results)
