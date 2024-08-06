from django.contrib import admin
from .models import *
from .forms import *
from django import forms
from django.utils.html import strip_tags  # Used for HTML content


class TeseEditForm(forms.ModelForm):
    class Meta:
        model = Tese
        fields = ['resumo', 'palavras_chave', 'areas', 'tecnologias', 'imagem', 'recil', 'relatorio', 'link_aplicacao']


class TeseAdmin(admin.ModelAdmin):

    list_display = ('numero_TFC', 'defesa_dia', 'defesa_hora', 'titulo', 'id', 'autores', 'ano', 'resumo_short', 'entidade_externa', 'imagem', 'video', 'relatorio')
    search_fields = ('titulo', 'autores',)
    list_editable = ('numero_TFC', 'defesa_dia', 'defesa_hora', 'autores', 'ano')
    list_filter = ['ano',]

    def resumo_short(self, obj):
        if obj.resumo:
            return strip_tags(obj.resumo[:100])  # Truncate to 100 characters and remove HTML tags
        return ''
    resumo_short.short_description = 'Resumo'  # Custom column name


#    def change_view(self, request, object_id, form_url='', extra_context=None):
#        if request.user.groups.filter(name='editor').exists():
#            self.form = TeseEditForm

#        return super().change_view(request, object_id, form_url, extra_context)

    filter_horizontal = ('orientadores', 'cursos', 'tecnologias', 'areas', 'palavras_chave')

admin.site.register(Tese, TeseAdmin)

admin.site.register(Ano)
admin.site.register(Ciclo)
admin.site.register(Curso)
admin.site.register(Area)
admin.site.register(PalavraChave)
admin.site.register(Tecnologia)
admin.site.register(Orientador)