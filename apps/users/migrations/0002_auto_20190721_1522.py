# Generated by Django 2.2 on 2019-07-21 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='female', max_length=10, verbose_name='性别'),
        ),
    ]