# Generated by Django 3.2.9 on 2021-11-28 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20211128_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kategoria',
            name='id_kategorii',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='klient',
            name='id_klienta',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='producent',
            name='id_producenta',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='produkt',
            name='id_produktu',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
