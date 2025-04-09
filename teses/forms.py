from django import forms
from django.forms import ModelForm
from .models import Tese, Area

class TeseForm(ModelForm):
    areas = forms.ModelMultipleChoiceField(
        queryset=Area.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = Tese
        fields = ['resumo', 'palavras_chave', 'areas', 'tecnologias']


# nao uso

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
