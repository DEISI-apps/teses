# Generated by Django 4.0.6 on 2023-10-22 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teses', '0005_tese_nota'),
    ]

    operations = [
        migrations.AddField(
            model_name='tese',
            name='autores',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Autor',
        ),
    ]