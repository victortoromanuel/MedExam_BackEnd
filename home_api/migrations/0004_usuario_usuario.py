# Generated by Django 3.2.11 on 2022-03-17 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_api', '0003_auto_20220221_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='Usuario',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
