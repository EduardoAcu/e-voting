# Generated by Django 4.1.1 on 2024-12-13 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_account_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='voted_main',
            new_name='voted_iei',
        ),
    ]
