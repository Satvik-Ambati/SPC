# Generated by Django 2.1.2 on 2018-10-24 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181024_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='accounts.ConsolePicture/bytes/filename/mimetype'),
        ),
    ]
