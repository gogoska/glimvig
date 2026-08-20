from django.apps import AppConfig


class PoemsConfig(AppConfig):
    name = 'poems'

    def ready(self):
        import poems.signals
