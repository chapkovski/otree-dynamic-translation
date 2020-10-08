from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass
class MyPage2(Page):
    pass




page_sequence = [
    MyPage,
    MyPage2
]
