# Generated by Django 2.2.2 on 2020-03-15 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_remove_scholarshipapplication_auth_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarshipapplication',
            name='year',
            field=models.PositiveIntegerField(default=2020),
        ),
    ]
