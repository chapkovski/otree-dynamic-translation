
.. code-block:: python
    :linenos:

    from django.utils import translation

    class TransMixin:
        def get_context_data(self, **context):
            user_language = self.session.config.get('language', 'en')
            translation.activate(user_language)
            return super().get_context_data(**context)

    class Page(TransMixin, Page):
        pass

    class WaitPage(TransMixin, WaitPage):
        pass
