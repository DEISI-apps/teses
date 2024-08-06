from django.shortcuts import render, redirect
import os
import json
from .models import *
from .forms import TeseForm

file_name = 'tfcs_21-22.json'

app_directory = os.path.dirname(__file__)
json_file_path = os.path.join(app_directory, file_name)

with open(json_file_path) as f:
    tfcs = json.load(f)


def carrega_orientadores():

    orientadores = set()
    for tfc in tfcs:
        orientadores.add(tfc['orientador'])

    for orientador in orientadores:
        if not Orientador.objects.filter(nome=orientador).exists():
            Orientador.objects.create(nome=orientador)


def carrega_teses():

    curso = Curso.objects.get(nome= 'Licenciatura em Engenharia Informática')

    for tfc in tfcs:
        if Tese.objects.filter(numero=tfc['tfc']).exists():
            continue

        tese = Tese(
                numero = tfc['tfc'],
                titulo = tfc['Titulo'],
                entidade_externa = tfc['entidade'],
                autores = ' e '.join(tfc['autores']),
                avaliacao = tfc['final'],
                relatorio = tfc['relatorio'],
                ano = Ano.objects.get(ano = tfc['ano']),
        )

        if tfc['entidade']  != 'N/A':
            tese.entidade = tfc['entidade']

        if 'video' in tfc:
            tese.video = tfc['video']

        tese.save()

        tese.orientadores.add(Orientador.objects.get(nome=tfc['orientador']))
        tese.cursos.add(curso)

        tese.save()



def index_view(request):

    #carrega_orientadores()
    #carrega_teses()

    context = {
        'tfcs': Tese.objects.filter(cursos__ciclo__numero=1).order_by('-ano__ano','autores'),
        'mscs': Tese.objects.filter(cursos__ciclo__numero=2).order_by('-ano__ano','autores'),
        'phds': Tese.objects.filter(cursos__ciclo__numero=3).order_by('-ano__ano','autores'),
        }

    return render(request, 'teses/index.html', context)


def extract_view(request):

    #carrega_orientadores()
    #carrega_teses()

    for tese in Tese.objects.filter(cursos__ciclo__numero=1):
        if tese.resumo:
            tese.resumo = " ".join(tese.resumo.split())


        tese.autores = tese.autores.capitalize()
        tese.save()

    context = {
        'tfcs': Tese.objects.filter(cursos__ciclo__numero=1).order_by('-ano__ano','autores'),
        'mscs': Tese.objects.filter(cursos__ciclo__numero=2).order_by('-ano__ano','autores'),
        'phds': Tese.objects.filter(cursos__ciclo__numero=3).order_by('-ano__ano','autores'),
        }

    return render(request, 'teses/extract.html', context)

def extract_defesas_view(request):

    for tese in Tese.objects.filter(cursos__ciclo__numero=1):
        if tese.resumo:
            tese.resumo = " ".join(tese.resumo.split())

        tese.autores = tese.autores.capitalize()
        tese.save()

    tfcs_agendados = Tese.objects.filter(cursos__ciclo__numero=1, ano__ano='2024').exclude(defesa_dia=None).distinct().order_by('-ano__ano','defesa_dia','defesa_hora','numero_TFC')
    tfcs_por_agendar = Tese.objects.filter(cursos__ciclo__numero=1, ano__ano='2024').filter(defesa_dia=None).distinct()

    context = {
        'tfcs': list(tfcs_agendados) + list(tfcs_por_agendar),
        }

    return render(request, 'teses/extract_defesas.html', context)


from django.core.files.storage import FileSystemStorage


def edita_view(request, tese_id):

    f = open('logger.txt', 'a')
    f.write("\n\nentrada\n")
    f.write("\n\n")
    f.close()

    tese = Tese.objects.get(id=tese_id)
    context = {'tese': tese}

    return render(request, 'teses/edita.html', context)




import requests
from django.http import JsonResponse

def download_teses_BD_Alves_json(request):
    # Fazendo a solicitação à API com o token
    headers = {'x-api-token': 'cody2024'}
    url = 'https://deisi.ulusofona.pt/tfc/api/all'
    response = requests.get(url, headers=headers)

    # Verificando se a solicitação foi bem sucedida
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        data = response.json()
        return JsonResponse(data)
    else:
        # Caso a solicitação falhe, retornar um JSON com uma mensagem de erro
        error_message = {'error': 'Erro ao acessar a API'}
        return JsonResponse(error_message, status=response.status_code)
