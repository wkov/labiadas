# Generated by Django 2.2.1 on 2019-05-25 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('romani', '0118_auto_20190518_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comanda',
            name='format',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='romani.TipusProducte'),
        ),
        migrations.AlterField(
            model_name='comanda',
            name='frequencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='romani.Frequencia'),
        ),
        migrations.AlterField(
            model_name='diaproduccio',
            name='node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='romani.Node'),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='dia_produccio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entregas', to='romani.DiaProduccio'),
        ),
        migrations.AlterField(
            model_name='entrega',
            name='franja_horaria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='romani.FranjaHoraria'),
        ),
        migrations.AlterField(
            model_name='node',
            name='frequencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='romani.Frequencia'),
        ),
        migrations.AlterField(
            model_name='producte',
            name='etiqueta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='romani.Etiqueta'),
        ),
        migrations.AlterField(
            model_name='producte',
            name='frequencies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='romani.Frequencia'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lloc_entrega',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_profiles', to='romani.Node'),
        ),
    ]
