# Generated by Django 4.0.6 on 2025-03-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teses', '0034_alter_tese_relatorio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tese',
            name='relatorio',
            field=models.FileField(upload_to='teses/'),
        ),
    ]
