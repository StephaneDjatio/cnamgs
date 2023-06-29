from django.contrib import admin
from django.apps import apps

# Register your models here.
gestion_model = apps.get_app_config('gestion').get_models()

for model in gestion_model:
    admin.site.register(model)
