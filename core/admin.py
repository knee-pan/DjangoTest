from django.contrib import admin

from . import models

# Register your models here.


# list_display = ["__all__"]
# search_fields = ["headline"]

# @admin.display(
# boolean=True,
# ordering='pub_date',
# description='Published recently?',)


admin.site.register(models.Article)
admin.site.register(models.Author)
admin.site.register(models.Comment)
admin.site.register(models.Company)
