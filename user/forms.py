# -*- coding: utf-8 -*-
import hashlib, time
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from poetry.models import Poem, Theme
from user.models import Contributor

my_default_errors = {
    'required': 'Еңгізуге міндетті параметр'
}

error_messages = {'required': 'Толтыруға маңызды параметр'}


class UserAuthenticateForm(forms.ModelForm):
    email = forms.EmailField(required=True, error_messages=error_messages)
    password = forms.CharField(
        required=True,
        label='Құпиясөз',
        error_messages=error_messages,
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'Email',
            'password': 'Құпиясөз',
        }


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, error_messages=error_messages)
    full_name = forms.CharField(required=True, label='Есіміңіз', error_messages=error_messages)
    password1 = forms.CharField(required=True, label='Құпиясөз', widget=forms.PasswordInput,
                                error_messages=error_messages)
    password2 = forms.CharField(required=True, label='Құпиясөзді қайталаңыз', widget=forms.PasswordInput,
                                error_messages=error_messages)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = user.email
        user.is_active = 0
        hash = '%s%s' % (user.email, time.time())

        if commit:
            user.save()
            user.contributor = Contributor(user_id=user, full_name=self.cleaned_data["full_name"],
                                           activation_code=hashlib.md5(hash.encode('utf-8')).hexdigest())
            user.contributor.save()
            group = self.get_user_group()
            user.groups.add(group)
        else:
            pass

        return user

    def get_user_group(self):
        return Group.objects.get(name='site-users')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            raise forms.ValidationError("Бұл email-мен колднушы тіркелген.")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("Құпиясөзді растаңыз")
        if password1 != password2:
            raise forms.ValidationError("Құпиясөздер бір біріне сәйкес емес. Қайта теріңіз")

        if len(password2) < 6:
            raise forms.ValidationError('Кемінде 6 символ')

        return super(UserCreateForm, self).clean_password2()


class UserEditForm(forms.ModelForm):
    text_status = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),
        label='Сайттағы статусыңыз (250 символ)',
        error_messages=error_messages)

    class Meta:
        model = Contributor
        fields = ('full_name', 'text_status')
        labels = {
            'full_name': 'Есіміңіз',
            'text_status': 'Сайттағы статусыңыз (250 символ)',
        }
        error_messages = {
            'full_name': error_messages
        }


class OfferPoemFrom(forms.ModelForm):
    theme = forms.MultipleChoiceField(
        label="Тақырып",
        widget=forms.SelectMultiple,
        error_messages=error_messages,
        choices=Theme.objects.values_list('id', 'name').all()
    )

    class Meta:
        model = Poem
        fields = ('author', 'title', 'content', 'theme',)
        labels = {
            'author': 'Автор',
            'title': 'Шығарма аты',
            'content': 'Текст',
        }
        error_messages = {
            'author': error_messages,
            'title': error_messages,
            'content': error_messages,
            'theme': error_messages
        }
