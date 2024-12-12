# Generated by Django 4.1.1 on 2024-12-12 03:02

from django.conf import settings
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IEI_Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modal_id', models.CharField(default=main.models.modalID_generator, editable=False, max_length=50)),
                ('fullname', models.CharField(max_length=50)),
                ('photo', models.ImageField(blank=True, upload_to='candidates')),
                ('bio', models.TextField(null=True)),
                ('position', models.TextField(choices=[('Delegado Estudiantil', 'Delegado Estudiantil')], null=True)),
                ('voters', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='ceit_candidate',
            name='voters',
        ),
        migrations.RemoveField(
            model_name='cot_candidate',
            name='voters',
        ),
        migrations.RemoveField(
            model_name='cte_candidate',
            name='voters',
        ),
        migrations.RemoveField(
            model_name='mainssg_candidate',
            name='voters',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='auditor',
            new_name='delegado_estudiantil',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='businessmanager',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='governor',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='peaceofficer',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='pio',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='secretary',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='treasurer',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='vice_governor',
        ),
        migrations.AlterField(
            model_name='votingschedule',
            name='department',
            field=models.TextField(choices=[('Ingenieria Informatica', 'Ingenieria Informatica')], null=True),
        ),
        migrations.DeleteModel(
            name='CAS_Candidate',
        ),
        migrations.DeleteModel(
            name='CEIT_Candidate',
        ),
        migrations.DeleteModel(
            name='COT_Candidate',
        ),
        migrations.DeleteModel(
            name='CTE_Candidate',
        ),
        migrations.DeleteModel(
            name='MAINSSG_Candidate',
        ),
    ]
