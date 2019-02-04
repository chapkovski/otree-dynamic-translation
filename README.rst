

oTree apps: Switch languages without changing settings
=======================================================


Here is an example how to build an app that can change the language
based on a parameter set when you start the session.

First three sections of the following doc will cover general points
how to translate projects and apps in oTree using standard Django tools.

The last one covers this specific app and how to switch between languages
dynamically: in this case you can have several sessions with different languages
simultaneously without the need to restart the server after changing the
``settings.py``.

But first a small intro:

In a few words, translation in oTree and in Django in general consists of
three steps:

1. Mark what pieces of text you want to translate.

2. Generate special files (called ``django.po``) for each language you want to translate to.

3. Translate :-).

4. Compile these ``django.po`` files to binary ``django.mo`` files so it can be
used by Django when a specific language is used.



1. Python code - things to do to make translation work
------------------------------------------------------

You need to do two simple things to mark strings for translation
in your Python code:

0. Add the following parameter to your ``settings.py``:

.. code-block:: python

    LANGUAGE_SESSION_KEY = '_language'

It is not necessary, but it will deal with the issue of correct translation
of the very last page a user sees when they click 'Next' at the last page.
(when they are informed that the study is finished).

1. Import corresponding Python method:

.. code-block:: python

    from django.utils.translation import ugettext_lazy as _

Note that we export a method called ``ugettext_lazy`` as ``_`` just to make
code more compact, but of course you can import it 'as it is' so to say:

.. code-block:: python

    from django.utils.translation import ugettext_lazy

So two following lines will produce exactly same result:

.. code-block:: python

    a = _('hello')
    a = ugettext_lazy('hello')


2. Actually **wrap** all strings you want to mark for translation into this method:

Here is an example of marking ``choices``, ``label``, and ``help_text`` parameters of
a field ``mood`` in our ``models.py`` file:

.. code-block:: python

    class Player(BasePlayer):
        mood = models.IntegerField(choices=[(0, _('Good')), (1, _('Bad'))],
                               label=_('Mood'),
                               help_text=_('Your mood today?'),
                               )

2. Templates - things to do to make translation work
--------------------------------------------------

If you want to translate certain blocks of text right
in your templates, you need to add a reference to ``i18n`` tag
library. So a typical heading of your oTree page will look like:

.. code-block:: django

 {% extends "global/Page.html" %}
 {% load otree  i18n %}


There are two main tags you need to use for translation:


``{% trans 'some_text %}``:
    To translate a string of text, you can use {% trans %} block,
    It should be in quotation marks and cannot include any variables.


``{% trans 'some_text %}``:
    it is more flexible alternative
    to ``{% trans %}`` block. You put any text between
    {% blocktrans %} and {% endblocktrans %} and it will be added
    to a file where messages for translation are stored.

.. code-block:: django

    {% blocktrans %} some text here {% endblocktrans %}


It can also include some variables, like the ones you pass
through ``vars_for_template`` method of a page.


.. code-block:: django

    {% blocktrans %} This player's payoff is {{ payoff }} {% endblocktrans %}

You need however pass it through ``vars_for_template`` to make it work.
The code below **won't** work:

.. code-block:: django

    {% blocktrans %}  ## WON'T WORK
        This player's payoff is {{ player.payoff }}
    {% endblocktrans %}


but what you can do to bypass this limitation is ``with`` parameter for ``blocktrans``:

.. code-block:: django

    {% blocktrans with payoff=player.payoff %}
        This player's payoff is {{ player.payoff }}
    {% endblocktrans %}

3. Create messages files (``django.po``) and compile them
------------------------------------------------------------------------

After marking is done, you go in your terminal (for Macos/Linux/Unix)
or PowerShell/command line tool (for Windows) and change to your oTree
project folder.

There you need to type first:

.. code-block:: bash

    otree makemessages -l LANG

where ``LANG`` should be changed to a language you intend to translate to
(`ru` for Russian, `fr` for French, `de` for German etc. Full list of language
codes can be found here_.

.. _here: http://www.i18nguy.com/unicode/language-identifiers.html

That will generate a folder ``locale`` in your project subfolder, with
corresponding subfolders for each language, and ``django.po`` files in it.

For each item that you marked it will generate two fields:

.. code-block::

    #: transapp/templates/transapp/Results.html:5
    msgid "Results"
    msgstr ""

Where you need to fill in ``msgstr`` field with actual translation. For Russian it will
look like:

.. code-block::

    #: transapp/templates/transapp/Results.html:5
    msgid "Results"
    msgstr "Результаты"


After you are done, you compile ready translation into binary files:

.. code-block:: bash

    otree compilemessages

and you are done! Your project is ready to switch to another language.

Standard way of doing it is to change ``LANGUAGE_CODE`` in your ``settings.py``
to another language:

.. code-block:: python

    LANGUAGE_CODE = 'ru'

But in the next section I'll show how to make switching dynamic so you can
have different sessions for the same app (or apps) on different languages.


4. Making language switching dynamic
----------------------------------------------------------------------

As you can see two configurations in our ``settings.py`` point out
to the same app (``transapp``), but the only difference is in
``language`` settings:

.. code:: python

    SESSION_CONFIGS = [
        {
            'name': 'transapp_en',
            'display_name': "transapp - English",
            'num_demo_participants': 2,
            'app_sequence': ['transapp'],
            'language':'en'
        },
        {
            'name': 'transapp_ru',
            'display_name': "transapp - Russian",
            'num_demo_participants': 2,
            'app_sequence': ['transapp'],
            'language': 'ru'
        },
    ]


In ``models.py`` I check that the parameter inserted by a user when
they create a session can be actually supported by existing translation:

.. code-block:: python


    TRNSL_ERR_MSG = 'Translation for this language does not exist'

    class Subsession(BaseSubsession):
        def creating_session(self):
            assert self.session.config.get('language', 'en') \
                   in Constants.translated_languages, TRNSL_ERR_MSG

It is *not* a necessary step, but just a precaution to be sure that no
rubbish will be inserted.


Then in ``pages.py`` we adjust standard oTree ``Page`` and ``WaitPage`` classes:

.. code-block:: python

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


Before showing the page or waiting page to a final user
the code reads a ``language`` parameter from ``session.config`` and activates
it for a corresponding page.


Minor things
============

# If you use translated choices for models, AND if you use dynamic switching, it is important
    # to use tuples, not simple lists (like [_('Good'), _('Bad')]), because otherwise when you switch the language
    # the allowed set of choices won't let user go further.