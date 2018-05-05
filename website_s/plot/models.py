from django.db import models
from django.forms import ModelForm
from math import pi

class Input(models.Model):
    K = models.CharField(verbose_name='Keyword', max_length=100)
    I = models.CharField(verbose_name='Interval', max_length=20)
    L = models.CharField(verbose_name='Length', max_length=20)

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = '__all__'

