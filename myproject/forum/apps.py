from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Setting up an automatic ID field for models
    name = 'forum'

    def ready(self):
        from . import signals  # Include signals.py so Django listens for user creation events


'''
This file is responsible for the setup and configuration of the application itself.
"from . import signals" - marked in grey but that's ok, because it is executed for the side effect of registering Django signals.
'''
