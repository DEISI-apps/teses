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
        fields = ['resumo', 'areas', 'tecnologias']




class TeseEditForm(forms.ModelForm):
    class Meta:
        model = Tese
        fields = ['resumo', 'areas', 'tecnologias', 'imagem', 'recil', 'relatorio', 'link']