# Generated by Django 2.2.2 on 2020-03-14 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_scholarshipapplication_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholarshipapplication',
            name='auth_user',
        ),
    ]