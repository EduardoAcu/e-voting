# Generated by Django 4.1.1 on 2024-12-13 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_ap_candidate_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votingschedule',
            name='department',
            field=models.TextField(choices=[('AP', 'AP')], null=True),
        ),
        migrations.DeleteModel(
            name='IEI_Candidate',
        ),
    ]
