# Generated by Django 3.0 on 2020-02-12 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('off_sub', '0003_auto_20200212_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
