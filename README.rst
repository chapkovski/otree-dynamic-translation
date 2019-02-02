an example how to switch languages without changing settings (based on session params)


Here is an example how to build an app that can change the language
based on a parameter set when you start the session.

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


