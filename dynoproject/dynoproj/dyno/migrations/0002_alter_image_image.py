# Generated by Django 4.1.1 on 2023-02-05 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dyno', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='dyno/images/'),
        ),
    ]