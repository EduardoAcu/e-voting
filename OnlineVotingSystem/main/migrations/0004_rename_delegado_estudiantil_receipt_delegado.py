# Generated by Django 4.1.1 on 2024-12-13 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_votingschedule_department_ap_candidate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='delegado_estudiantil',
            new_name='delegado',
        ),
    ]
