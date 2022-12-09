# Generated by Django 4.0.4 on 2022-12-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='doc_id',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo'), (2, 'Pagado')], verbose_name='Estado'),
        ),
    ]
