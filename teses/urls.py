from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('extract/', views.extract_view, name='extract'),
    path('extract_a_decorrer/', views.extract_a_decorrer_view, name='extract_a_decorrer'),
        path('entidades/', views.entidades_view, name='entidades'),
    path('extract_defesas/', views.extract_defesas_view, name='extract-defesas'),
    path('edita/<int:tese_id>', views.edita_view, name='edita'),
    path('download_json/', views.download_teses_BD_Alves_json, name='download_json'),
]