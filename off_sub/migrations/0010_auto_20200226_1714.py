# Generated by Django 3.0 on 2020-02-26 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('off_sub', '0009_auto_20200226_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
