from django.apps import AppConfig


class SoftdeskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'softdesk' 

        def ready(self):
        
        # Implicitly connect signal handlers decorated with @receiver. 
        from . import signals 
