# Generated by Django 4.0.6 on 2025-03-26 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teses', '0027_alter_tese_ano'),
    ]

    operations = [
        migrations.AddField(
            model_name='tese',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
