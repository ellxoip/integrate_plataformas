# Generated by Django 4.2.1 on 2023-06-06 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negocioCliente', '0002_provincia_comuna_provincia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
    ]
