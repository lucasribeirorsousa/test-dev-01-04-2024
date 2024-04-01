from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CalculatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calculator"
        
    def ready(self):
        from .signals import populate_consumers_from_excel
        
        post_migrate.connect(populate_consumers_from_excel, sender=self)
