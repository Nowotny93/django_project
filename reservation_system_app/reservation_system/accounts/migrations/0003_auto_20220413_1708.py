# Generated by Django 3.1.3 on 2022-04-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_reservationsystemuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationsystemuser',
            name='username',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]