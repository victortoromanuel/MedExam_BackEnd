# Generated by Django 3.2.11 on 2022-02-21 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preguntasxexamenxusuario',
            name='IdRespuesta',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home_api.respuesta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='respuesta',
            name='Valor',
            field=models.CharField(choices=[('C', 'Correcto'), ('I', 'Incorrecto')], default='I', max_length=15),
        ),
    ]
