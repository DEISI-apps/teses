from django.db import models
from django.contrib.auth.models import User


class Ano(models.Model):
    ano = models.CharField(max_length= 200)

    class Meta:
        ordering = ('-ano',)  # Order by 'ano' field

    def __str__(self):
        return f"{self.ano}"


class Ciclo(models.Model):
    numero = models.IntegerField()

    def __str__(self):
        return f"{self.numero}º Ciclo"


class Curso(models.Model):
    nome = models.CharField(max_length= 200)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name = 'cursos', blank=True, null=True)
    def __str__(self):
        return f"{self.nome}"


class Orientador(models.Model):
    nome = models.CharField(max_length= 200)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return f"{self.nome}"


class PalavraChave(models.Model):
    nome = models.CharField(max_length= 200)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return f"{self.nome}"

class Area(models.Model):
    nome = models.CharField(max_length= 200)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return f"{self.nome}"

class Tecnologia(models.Model):
    nome = models.CharField(max_length= 200)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return f"{self.nome}"


class Tese(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # 1 = ID do superusuário, por exemplo    defesa_dia = models.DateField(default=None, blank=True, null=True)
    defesa_dia = models.DateField(default=None, blank=True, null=True)
    defesa_hora = models.TimeField(default=None, blank=True, null=True)
    concluido = models.BooleanField(default=False, blank=True, null=True)
    titulo = models.CharField(max_length= 200)
    numero_TFC = models.CharField(max_length= 200, blank=True, null=True)
    autores = models.CharField(max_length= 200, default=None)
    email_contacto =  models.EmailField()
    orientadores = models.ManyToManyField(Orientador, related_name = 'teses')
    entidade_externa =  models.CharField(max_length= 300, blank=True, null=True)

    cursos = models.ManyToManyField(Curso, related_name = 'cursos')
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name = 'teses')

    resumo = models.TextField()

    palavras_chave =  models.ManyToManyField(PalavraChave, related_name = 'teses')
    areas =  models.ManyToManyField(Area, related_name = 'teses')
    tecnologias =  models.ManyToManyField(Tecnologia, related_name = 'teses')

    relatorio = models.FileField(upload_to="teses/", blank=True, null=True)
    apresentacao = models.FileField(upload_to="teses/", blank=True, null=True)

    imagem = models.ImageField(upload_to="teses/")
    video =  models.CharField(max_length= 200, blank=True, null=True)
    github = models.CharField(max_length= 200, blank=True, null=True)
    recil = models.CharField(max_length= 200, blank=True, null=True)
    link_aplicacao = models.CharField(max_length= 200, blank=True, null=True)

    avaliacao = models.CharField(max_length= 200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ('titulo',)


    def clean(self):
        # Corrigir resumo (remover espaços extras e quebras de linha estranhas)
        if self.resumo:
            self.resumo = " ".join(self.resumo.split())
        
        # Corrigir autores (retirar eventuais " e " capitalizar os autores)
        if self.autores:
            self.autores = self.autores.replace(' e ', ', ')
            self.autores = self.autores.capitalize()
        
        

    def __str__(self):
        return f"{self.titulo}, {self.autores}"



class Proposta(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # 1 = ID do superusuário, por exemplo    defesa_dia = models.DateField(default=None, blank=True, null=True)
    atribuida = models.BooleanField(default=False, blank=True, null=True)
    titulo = models.CharField(max_length= 200)
    orientadores = models.ManyToManyField(Orientador, related_name = 'propostas')
    email_contacto =  models.EmailField()
    entidade_externa =  models.CharField(max_length= 300, blank=True, null=True)

    cursos = models.ManyToManyField(Curso, related_name = 'propostas')
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name = 'propostas')

    resumo = models.TextField()

    palavras_chave =  models.ManyToManyField(PalavraChave, related_name = 'propostas')
    areas =  models.ManyToManyField(Area, related_name = 'propostas')
    tecnologias =  models.ManyToManyField(Tecnologia, related_name = 'propostas')

    imagem = models.ImageField(upload_to="propostas/")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ('titulo',)


    def clean(self):
        # Corrigir resumo (remover espaços extras e quebras de linha estranhas)
        if self.resumo:
            self.resumo = " ".join(self.resumo.split())
        
    @property
    def str_orientadores(self):
        return ', '.join([str(orientador) for orientador in self.orientadores.all()])

    def __str__(self):
        return f"{self.titulo}, {self.str_orientadores}"
