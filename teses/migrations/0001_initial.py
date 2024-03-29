# Generated by Django 4.0.6 on 2023-10-22 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tese',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('resumo', models.TextField()),
                ('pdf', models.CharField(blank=True, max_length=200, null=True)),
                ('recil', models.CharField(blank=True, max_length=200, null=True)),
                ('imagem', models.CharField(blank=True, max_length=200, null=True)),
                ('ano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teses', to='teses.ano')),
                ('ciclo_estudos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teses', to='teses.ciclo')),
            ],
        ),
        migrations.CreateModel(
            name='PalavraChave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palavra_chave', models.CharField(max_length=200)),
                ('tese', models.ManyToManyField(related_name='palavras_chave', to='teses.tese')),
            ],
        ),
        migrations.CreateModel(
            name='Orientador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('apelido', models.CharField(max_length=200)),
                ('teses', models.ManyToManyField(related_name='orientadores', to='teses.tese')),
            ],
        ),
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('apelido', models.CharField(max_length=200)),
                ('tese', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alunos', to='teses.tese')),
            ],
        ),
    ]
