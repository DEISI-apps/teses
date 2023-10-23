from django.db import models


class Ano(models.Model):
    ano = models.CharField(max_length= 200)

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

    def __str__(self):
        return f"{self.nome}"


class Area(models.Model):
    nome = models.CharField(max_length= 200)

    def __str__(self):
        return f"{self.nome}"

class Tecnologia(models.Model):
    nome = models.CharField(max_length= 200)

    def __str__(self):
        return f"{self.nome}"


class Tese(models.Model):
    numero = models.CharField(max_length= 200, blank=True, null=True)
    titulo = models.CharField(max_length= 200)
    resumo = models.TextField(blank=True, null=True)
    areas =  models.ManyToManyField(Area, related_name = 'teses')
    tecnologias =  models.ManyToManyField(Tecnologia, related_name = 'teses')
    orientadores = models.ManyToManyField(Orientador, related_name = 'teses')
    entidade_externa =  models.CharField(max_length= 300, blank=True, null=True)
    alunos = models.CharField(max_length= 200, blank=True, null=True)
    cursos = models.ManyToManyField(Curso, related_name = 'cursos')
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name = 'teses')
    relatorio = models.FileField(upload_to="", blank=True, null=True)
    imagem = models.ImageField(upload_to="", null=True, blank=True)
    video =  models.CharField(max_length= 200, blank=True, null=True)
    github = models.CharField(max_length= 200, blank=True, null=True)
    recil = models.CharField(max_length= 200, blank=True, null=True)
    link = models.CharField(max_length= 200, blank=True, null=True)
    avaliacao = models.CharField(max_length= 200, blank=True, null=True)

    def __str__(self):
        return f"{self.titulo}, {self.alunos}"
