from django.contrib import admin
from .models import *
from .forms import *
from django import forms
from django.utils.html import strip_tags  # Used for HTML content


class TeseEditForm(forms.ModelForm):
    class Meta:
        model = Tese
        fields = ['resumo', 'palavras_chave', 'areas', 'tecnologias', 'imagem', 'recil', 'relatorio', 'link_aplicacao']


class TeseAdminForm(forms.ModelForm):
    class Meta:
        model = Tese
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ano'].initial = Ano.objects.get_or_create(ano="2025")[0]


class TeseAdmin(admin.ModelAdmin):
    form = TeseAdminForm

    list_display = ('titulo', 'numero_TFC', 'get_ciclo', 'created_at', 'autores', 'ano', 'resumo_short', 'list_orientadores', 'entidade_externa', 'imagem', 'video', 'relatorio', 'defesa_dia', 'defesa_hora')
    search_fields = ('titulo', 'autores', 'orientadores', 'ano__ano', 'cursos__ciclo__numero', 'cursos__nome', 'tecnologias__nome', 'areas__nome', 'palavras_chave__nome')
    list_filter = ['cursos__ciclo', 'ano', 'orientadores']
    ordering = ['created_at', 'ano', 'numero_TFC']
    filter_horizontal = ('orientadores', 'cursos', 'tecnologias', 'areas', 'palavras_chave')
    exclude = ('owner', 'defesa_dia', 'defesa_hora', 'numero_TFC', 'recil', 'link_aplicacao', 'avaliacao')

    def get_ciclo(self, obj):
            # Aqui estamos a acessar o primeiro ciclo de um dos cursos associados à tese
            if obj.cursos.exists():
                return obj.cursos.first().ciclo.numero
            return None
    get_ciclo.short_description = 'Ciclo'
        
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


class PropostaAdmin(admin.ModelAdmin):
    exclude = ('owner',) 
    filter_horizontal = ('orientadores', 'cursos', 'tecnologias', 'areas', 'palavras_chave')

admin.site.register(Proposta, PropostaAdmin)