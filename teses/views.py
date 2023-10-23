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
                alunos = ' e '.join(tfc['alunos']),
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

    context = {'teses': Tese.objects.all().order_by('numero'),
        }

    return render(request, 'teses/index.html', context)

from django.core.files.storage import FileSystemStorage

def edita_view(request, tese_id):

    f = open('logger.txt', 'a')
    f.write("\n\nentrada\n")
    tese = Tese.objects.get(id=tese_id)

    form = TeseForm(request.POST or None, request.FILES, instance=tese)

    f.write(f"form.is_valid(): {form.is_valid()}\n")

    f.write(f"tese: {tese}\n")

    f.write(f"request.POST: {request.POST}\n")


    if request.method == 'POST' and form.is_valid():

            tese = form.save(commit=False)

            tese.resumo = '\r\n\r\n'.join([paragrafo.replace('\r\n',' ') for paragrafo in tese.resumo.split('\r\n\r\n')])
            tese.save()

            uploaded_file = request.FILES.get('imagem')
            if uploaded_file:
                # Create a unique filename for the uploaded file, e.g., based on tese_id
                unique_filename = f'TFC_{tese.ano.ano[:2]}_{tese_id}_{uploaded_file.name}'

                # Save the file to the designated folder (MEDIA_ROOT)
                fs = FileSystemStorage()
                filename = fs.save(unique_filename, uploaded_file)
                tese.imagem = filename  # Store the filename in your model
                tese.save()

            # Process new keywords
            new_keywords = request.POST.getlist('new_keywords')
            for keyword in new_keywords:
                if keyword:
                    for k in keyword.split(';'):
                        # Create a new PalavraChave object
                        new_keyword = PalavraChave.objects.create(nome=k.strip())
                        # Associate the new keyword with the Tese
                        tese.palavras_chave.add(new_keyword)


            return redirect('index')


    context = {'tese': tese, 'form': form, 'tese_id': tese_id}
    f.write("\n\n")
    f.close()


    return render(request, 'teses/edita.html', context)



