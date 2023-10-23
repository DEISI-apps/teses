from django.contrib import admin

# Register your models here.
from .models import *
from .forms import *
from django.utils.html import strip_tags  # Used for HTML content



admin.site.register(Ano)
admin.site.register(Ciclo)
admin.site.register(Curso)

class TeseAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'alunos', 'resumo_short', 'imagem', 'relatorio')

    def resumo_short(self, obj):
        if obj.resumo:
            return strip_tags(obj.resumo[:100])  # Truncate to 100 characters and remove HTML tags
        return ''
    resumo_short.short_description = 'Resumo'  # Custom column name

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.groups.filter(name='editor').exists():
            self.form = TeseEditForm

        return super().change_view(request, object_id, form_url, extra_context)
    #filter_horizontal = ('tecnologias', 'areas')

admin.site.register(Tese, TeseAdmin)

admin.site.register(Area)
admin.site.register(Tecnologia)
admin.site.register(Orientador)