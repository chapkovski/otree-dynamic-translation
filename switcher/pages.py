from .generic_pages import Page



class MyPage(Page):
    form_model = 'player'
    form_fields = ['age']


class MyPage2(Page):
    pass


page_sequence = [
    MyPage,
    MyPage2
]
