from django.contrib import admin
from . import models


class PoetAdmin(admin.ModelAdmin):
    exclude = ['letter', 'slug']
    list_filter = ['age', 'sex', 'is_active']
    search_fields = ['name']


class PoemAdmin(admin.ModelAdmin):
    exclude = ['added_user']
    list_filter = ['is_shown']
    search_fields = ['title', 'content']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_user = request.user

        obj.save()


admin.site.register(models.Age)
admin.site.register(models.Poem, PoemAdmin)
admin.site.register(models.Poet, PoetAdmin)
admin.site.register(models.Theme)
