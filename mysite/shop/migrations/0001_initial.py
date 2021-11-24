# Generated by Django 3.2.9 on 2021-11-24 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Czat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('klient', models.IntegerField()),
                ('producent', models.IntegerField()),
            ],
            options={
                'unique_together': {('klient', 'producent')},
            },
        ),
        migrations.CreateModel(
            name='Kategoria',
            fields=[
                ('id_kategorii', models.IntegerField(primary_key=True, serialize=False)),
                ('nazwa_kategorii', models.CharField(default='null', max_length=50)),
                ('id_nadkategorii', models.IntegerField()),
                ('podkategoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.kategoria')),
            ],
        ),
        migrations.CreateModel(
            name='Klient',
            fields=[
                ('id_klienta', models.IntegerField(primary_key=True, serialize=False)),
                ('imie', models.CharField(default='null', max_length=50, verbose_name='imię')),
                ('nazwisko', models.CharField(default='null', max_length=50)),
                ('adres_dostawy', models.CharField(default='null', max_length=50)),
                ('login', models.CharField(max_length=50)),
                ('haslo', models.CharField(max_length=50, verbose_name='hasło')),
            ],
        ),
        migrations.CreateModel(
            name='Producent',
            fields=[
                ('id_producenta', models.IntegerField(primary_key=True, serialize=False)),
                ('imie', models.CharField(default='null', max_length=50, verbose_name='imię')),
                ('nazwisko', models.CharField(default='null', max_length=50)),
                ('adres', models.CharField(default='null', max_length=50)),
                ('login', models.CharField(max_length=50)),
                ('haslo', models.CharField(max_length=50, verbose_name='hasło')),
            ],
        ),
        migrations.CreateModel(
            name='Reklamacja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tresc', models.CharField(max_length=1000, verbose_name='treść')),
                ('typ_reklamacji', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Wiadomosc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tresc', models.CharField(max_length=50, verbose_name='treść')),
                ('data', models.DateField()),
                ('czy_odczytana', models.BooleanField(default=False)),
                ('flaga', models.BooleanField()),
                ('czat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.czat')),
            ],
        ),
        migrations.CreateModel(
            name='Zamowienie',
            fields=[
                ('klient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='shop.klient')),
                ('czy_oplacone', models.BooleanField(verbose_name='czy opłacone')),
                ('sposob_dostawy', models.CharField(max_length=50, verbose_name='sposób dostawy')),
                ('status', models.IntegerField()),
                ('koszt', models.FloatField()),
                ('czat', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.czat')),
                ('producent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.producent')),
                ('reklamacja', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.reklamacja')),
            ],
        ),
        migrations.CreateModel(
            name='Produkt',
            fields=[
                ('id_produktu', models.IntegerField(primary_key=True, serialize=False)),
                ('numer_partii', models.IntegerField()),
                ('cena', models.FloatField()),
                ('opis', models.CharField(blank=True, max_length=1000)),
                ('kategoria', models.ManyToManyField(to='shop.Kategoria')),
                ('producent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.producent')),
                ('zamowienie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.zamowienie', verbose_name='zamówienie')),
            ],
        ),
    ]
