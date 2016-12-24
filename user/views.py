from . import forms as userforms
from .models import Contributor
from django.http import Http404
from django.db.models import Count
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import generic
from django.views.generic import CreateView, UpdateView


class SignUpView(generic.View):
    form_class = userforms.UserCreateForm
    template_name = "user/signup.html"
    success_url = reverse_lazy('user:user_home')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class
        })

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            subject = "PoetryDB: Қолданушы активациясы"
            to = [user.email]
            from_email = settings.EMAIL_HOST_USER
            url = request.build_absolute_uri(
                reverse('user:user_activate', args = [user.id, user.contributor.activation_code]))

            ctx = {
                'url': url,
                'user': user,
            }

            message = get_template('user/auth/activation_email.html').render(ctx)
            msg = EmailMessage(subject, message, to = to, from_email = from_email)
            msg.content_subtype = 'html'
            msg.send()

            messages.info(request,
                          'Сайтта тіркелу сәтті өтті. Email-адресіңізге активация сілтемесі жіберілді. Рахмет!')

            return redirect(reverse('user:user_login'))

        return render(request, self.template_name, {
            'form': form
        })


class IndexView(generic.View):
    template_name = "user/index.html"

    def get(self, request, *args, **kwargs):
        contributor = Contributor.objects.filter(user_id = kwargs.get('pk'), user__is_active = 1).get()

        return render(request, self.template_name, {
            'contributor': contributor
        })


class LoginView(generic.View):
    form_class = userforms.UserAuthenticateForm
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class
        })

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            auth_user = authenticate(username = email, password = password)

            if auth_user is not None:
                if auth_user.is_active:
                    login(request, auth_user)

                    return redirect(reverse('user:user_home', args = [auth_user.id]))
                else:
                    messages.info(request, 'Сіздің аккаунтыңыз активациядан өтпеді.')
            else:
                messages.error(request, 'Email немесе құпиясөз қате терілген. Тағыда қайталап көріңіз')

            return redirect(reverse('user:user_login'))

        return render(request, self.template_name, {
            'form': form
        })


class ActivateView(generic.View):
    template_name = 'user/activate.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        activation_code = kwargs.get('hash')
        message = ''
        css_class = 'alert-success'

        contributor = Contributor.objects.filter(user_id = user_id).get()

        if contributor.activation_code != '' and contributor.user.is_active == 0:
            if contributor.activation_code != activation_code:
                message = 'Активациялық код дұрыс емес'
                css_class = 'alert-warning'
            else:
                contributor.activation_code = ''
                contributor.user.is_active = 1
                contributor.save()
                contributor.user.save()
                message = 'Активация сәтті өтті. Қош келдіңіз'
        else:
            message = 'Сіз сайтың тексерілген мүшесісіз'
            css_class = 'alert-info'

        return render(request, self.template_name, {
            'message': message,
            'css_class': css_class
        })


class AllPoemsView(generic.View):
    template_name = 'user/all_added_poems.html'

    def get(self, request, *args, **kwargs):
        contributor = Contributor.objects.filter(user_id = kwargs.get('pk'), user__is_active = 1).get()

        return render(request, self.template_name, {
            'contributor': contributor
        })


class OfferPoem(SuccessMessageMixin, CreateView):
    form_class = userforms.OfferPoemFrom
    template_name = 'user/offer_poem.html'
    success_message = 'Шығарма базамызға қосылды, модерациядан кейін жалпы тізімде орнын табады. Рахмет =)'

    def get_context_data(self, **kwargs):
        context = super(OfferPoem, self).get_context_data(**kwargs)
        context['contributor'] = self.request.user.contributor

        return context

    def form_valid(self, form):
        form.instance.added_user = self.request.user

        return super(OfferPoem, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('user:offer_poem')


class EditUserView(SuccessMessageMixin, UpdateView):
    model = Contributor
    form_class = userforms.UserEditForm
    success_message = 'Жеке ақпаратыңыз сәтті түрде оңделді. =)'

    def get_object(self, queryset = None):
        if int(self.request.user.id) != int(self.kwargs['pk']):
            raise Http404("Сіз тек өз аккаунтыңызды өңдей аласыз")

        obj = Contributor.objects.get(user_id = self.request.user)

        return obj

    def get_success_url(self):
        return reverse_lazy('user:edit_profile', args = [self.kwargs.get('pk')])


class TopContributors(generic.View):
    template_name = 'user/top_contributors.html'

    def get(self, request, *args, **kwargs):
        # users = (User.objects
        #          .filter(is_active = 1)
        #          .values('id', 'contributor__full_name')
        #          .annotate(Count("id"), poems_count = Count('poem__id'))
        #          .order_by('-poems_count'))
        users = User.objects.raw('''
	            SELECT
	                users.id, uc.full_name as contributor__full_name, COUNT(poem.id) as poems_count
	            FROM
	                auth_user as users
	            JOIN user_contributor as uc ON uc.user_id=users.id
	            JOIN poetry_poem as poem ON poem.added_user_id=users.id AND poem.is_shown=1
	            WHERE users.is_active=1
	            GROUP BY users.id
	            ORDER BY poems_count DESC
	        ''')
        return render(request, self.template_name, {
            'users': users
        })
