# Generated by Django 2.1.2 on 2018-10-24 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20181024_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='filename',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]