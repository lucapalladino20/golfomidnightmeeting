from django.contrib import admin
from django.apps import apps

# Register your models here.
app = apps.get_app_config('theme_pixel')

for model in app.get_models():
    admin.site.register(model, admin.ModelAdmin)