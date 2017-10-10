from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Contributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    text_status = models.CharField(max_length=250, blank=True)
    avatar = models.ImageField(upload_to='uploads/', blank=True, verbose_name='Аватар')
    activation_code = models.CharField(blank=True, max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user:user_home', args=[self.id])
