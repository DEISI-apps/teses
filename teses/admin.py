from django.contrib import admin
from .models import *
from .forms import *
from django import forms
from django.utils.html import strip_tags  # Used for HTML content


class TeseEditForm(forms.ModelForm):
    class Meta:
        model = Tese
        fields = ['resumo', 'palavras_chave', 'areas', 'tecnologias', 'imagem', 'recil', 'relatorio', 'link_aplicacao']


class TeseAdmin_old(admin.ModelAdmin):

    list_display = ('titulo', 'numero_TFC', 'created_at', 'autores', 'ano', 'resumo_short', 'list_orientadores', 'entidade_externa', 'imagem', 'video', 'relatorio', 'defesa_dia', 'defesa_hora')
    search_fields = ('titulo', 'autores',)
#    list_editable = ('numero_TFC', 'defesa_dia', 'defesa_hora', 'autores', 'ano')
    list_filter = ['ano', 'orientadores']

    # Sort by 'ano' (descending) and 'numero_TFC' (ascending)
    ordering = ['ano', 'numero_TFC']

    def resumo_short(self, obj):
        if obj.resumo:
            return strip_tags(obj.resumo[:100])  # Truncate to 100 characters and remove HTML tags
        return ''
    resumo_short.short_description = 'Resumo'  # Custom column name


    # Custom method to display Many-to-Many field 'orientadores'
    def list_orientadores(self, obj):
        return ", ".join([orientador.nome for orientador in obj.orientadores.all()])
    list_orientadores.short_description = 'Orientadores'



#    def change_view(self, request, object_id, form_url='', extra_context=None):
#        if request.user.groups.filter(name='editor').exists():
#            self.form = TeseEditForm

#        return super().change_view(request, object_id, form_url, extra_context)

    filter_horizontal = ('orientadores', 'cursos', 'tecnologias', 'areas', 'palavras_chave')

class TeseAdminForm(forms.ModelForm):
    class Meta:
        model = Tese
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ano'].initial = Ano.objects.get_or_create(ano="2025")[0]


class TeseAdmin(admin.ModelAdmin):
    form = TeseAdminForm

    list_display = ('titulo', 'numero_TFC', 'created_at', 'autores', 'ano', 'resumo_short', 'list_orientadores', 'entidade_externa', 'imagem', 'video', 'relatorio', 'defesa_dia', 'defesa_hora')
    search_fields = ('titulo', 'autores',)
    list_filter = ['ano', 'orientadores']
    ordering = ['ano', 'numero_TFC']
    filter_horizontal = ('orientadores', 'cursos', 'tecnologias', 'areas', 'palavras_chave')
    exclude = ('owner', 'defesa_dia', 'defesa_hora', 'numero_TFC', 'recil', 'link_aplicacao', 'avaliacao')

    def resumo_short(self, obj):
        return strip_tags(obj.resumo[:100]) if obj.resumo else ''
    resumo_short.short_description = 'Resumo'

    def list_orientadores(self, obj):
        return ", ".join([orientador.nome for orientador in obj.orientadores.all()])
    list_orientadores.short_description = 'Orientadores'

    def get_queryset(self, request):
        """Mostrar apenas teses do próprio utilizador, exceto para superusuários."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        """Definir automaticamente o owner ao criar uma tese."""
        if not change:
            obj.owner = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        """Restringir edição a teses do próprio utilizador."""
        if obj is None:
            return True
        return obj.owner == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Restringir exclusão a teses do próprio utilizador."""
        if obj is None:
            return True
        return obj.owner == request.user or request.user.is_superuser


admin.site.register(Tese, TeseAdmin)

admin.site.register(Ano)
admin.site.register(Ciclo)
admin.site.register(Curso)
admin.site.register(Area)
admin.site.register(PalavraChave)
admin.site.register(Tecnologia)
admin.site.register(Orientador)