# Generated by Django 3.2.9 on 2022-01-13 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_zamowienie_id_zamowienie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kategoria',
            name='id_nadkategorii',
            field=models.IntegerField(null=True),
        ),
    ]
