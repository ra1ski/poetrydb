from django import forms
from django.contrib import admin
from . import models


class ContributorForm(forms.ModelForm):
    text_status = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))

    class Meta:
        model = models.Contributor
        fields = '__all__'


class ContributorAdmin(admin.ModelAdmin):
    form = ContributorForm
    search_fields = ['user__username']


admin.site.register(models.Contributor, ContributorAdmin)
