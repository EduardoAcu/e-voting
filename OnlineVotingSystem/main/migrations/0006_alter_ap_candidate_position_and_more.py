# Generated by Django 4.1.1 on 2024-12-13 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_ap_candidate_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ap_candidate',
            name='position',
            field=models.TextField(choices=[('delegado', 'Delegado Estudiantil')], null=True),
        ),
        migrations.AlterField(
            model_name='iei_candidate',
            name='position',
            field=models.TextField(choices=[('delegado', 'Delegado Estudiantil')], null=True),
        ),
    ]