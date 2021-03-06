# Generated by Django 3.2.9 on 2021-12-29 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('is_producent', models.BooleanField(default=False)),
                ('is_klient', models.BooleanField(default=False)),
                ('imie', models.CharField(default='null', max_length=50, verbose_name='imię')),
                ('nazwisko', models.CharField(default='null', max_length=50)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=50)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Czat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Kategoria',
            fields=[
                ('id_kategorii', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa_kategorii', models.CharField(default='null', max_length=50)),
                ('id_nadkategorii', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Produkt',
            fields=[
                ('nazwa', models.CharField(max_length=50)),
                ('id_produktu', models.AutoField(primary_key=True, serialize=False)),
                ('numer_partii', models.IntegerField()),
                ('cena', models.FloatField()),
                ('opis', models.CharField(blank=True, max_length=1000)),
                ('liczba', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
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
            name='Zamowienie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_zamowienie', models.IntegerField(null=True)),
                ('czy_oplacone', models.BooleanField(verbose_name='czy opłacone')),
                ('sposob_dostawy', models.CharField(max_length=50, verbose_name='sposób dostawy')),
                ('status', models.IntegerField()),
                ('koszt', models.FloatField()),
                ('czat', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.czat')),
                ('reklamacja', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.reklamacja')),
            ],
        ),
        migrations.CreateModel(
            name='Klient',
            fields=[
                ('id_klienta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='shop.user')),
                ('adres_dostawy', models.CharField(default='null', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Producent',
            fields=[
                ('id_producenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='shop.user')),
                ('adres', models.CharField(default='null', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ZamowienieProdukt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('produkt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.produkt')),
                ('zamowienie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.zamowienie')),
            ],
        ),
        migrations.CreateModel(
            name='Wiadomosc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_wiadomosc', models.IntegerField(null=True)),
                ('tresc', models.CharField(max_length=50, verbose_name='treść')),
                ('data', models.DateField()),
                ('czy_odczytana', models.BooleanField(default=False)),
                ('flaga', models.BooleanField()),
                ('czat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.czat')),
            ],
        ),
        migrations.AddIndex(
            model_name='reklamacja',
            index=models.Index(fields=['tresc'], name='shop_reklam_tresc_8b7d73_idx'),
        ),
        migrations.AddIndex(
            model_name='reklamacja',
            index=models.Index(fields=['typ_reklamacji'], name='shop_reklam_typ_rek_29b9ec_idx'),
        ),
        migrations.AddIndex(
            model_name='reklamacja',
            index=models.Index(fields=['status'], name='shop_reklam_status_199079_idx'),
        ),
        migrations.AddField(
            model_name='produkt',
            name='kategoria',
            field=models.ManyToManyField(to='shop.Kategoria'),
        ),
        migrations.AddField(
            model_name='kategoria',
            name='podkategoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.kategoria'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['imie'], name='shop_user_imie_047c3a_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['nazwisko'], name='shop_user_nazwisk_cf2997_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='shop_user_email_115a61_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='shop_user_usernam_05ef46_idx'),
        ),
        migrations.AddField(
            model_name='zamowienie',
            name='klient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.klient'),
        ),
        migrations.AddField(
            model_name='zamowienie',
            name='producent',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.producent'),
        ),
        migrations.AddIndex(
            model_name='wiadomosc',
            index=models.Index(fields=['tresc'], name='shop_wiadom_tresc_8b9f5a_idx'),
        ),
        migrations.AddIndex(
            model_name='wiadomosc',
            index=models.Index(fields=['data'], name='shop_wiadom_data_4914c0_idx'),
        ),
        migrations.AddIndex(
            model_name='wiadomosc',
            index=models.Index(fields=['czy_odczytana'], name='shop_wiadom_czy_odc_0a83c8_idx'),
        ),
        migrations.AddIndex(
            model_name='wiadomosc',
            index=models.Index(fields=['flaga'], name='shop_wiadom_flaga_045169_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='wiadomosc',
            unique_together={('id_wiadomosc', 'czat')},
        ),
        migrations.AddField(
            model_name='produkt',
            name='producent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.producent'),
        ),
        migrations.AddIndex(
            model_name='producent',
            index=models.Index(fields=['adres'], name='shop_produc_adres_a3bb97_idx'),
        ),
        migrations.AddIndex(
            model_name='klient',
            index=models.Index(fields=['adres_dostawy'], name='shop_klient_adres_d_cdc98f_idx'),
        ),
        migrations.AddIndex(
            model_name='kategoria',
            index=models.Index(fields=['nazwa_kategorii'], name='shop_katego_nazwa_k_d75277_idx'),
        ),
        migrations.AddField(
            model_name='czat',
            name='klient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.klient'),
        ),
        migrations.AddField(
            model_name='czat',
            name='producent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.producent'),
        ),
        migrations.AddIndex(
            model_name='zamowienie',
            index=models.Index(fields=['czy_oplacone'], name='shop_zamowi_czy_opl_7067d3_idx'),
        ),
        migrations.AddIndex(
            model_name='zamowienie',
            index=models.Index(fields=['sposob_dostawy'], name='shop_zamowi_sposob__92aa15_idx'),
        ),
        migrations.AddIndex(
            model_name='zamowienie',
            index=models.Index(fields=['status'], name='shop_zamowi_status_87fd14_idx'),
        ),
        migrations.AddIndex(
            model_name='zamowienie',
            index=models.Index(fields=['koszt'], name='shop_zamowi_koszt_4a2bab_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='zamowienie',
            unique_together={('id_zamowienie', 'klient')},
        ),
        migrations.AddIndex(
            model_name='produkt',
            index=models.Index(fields=['nazwa'], name='shop_produk_nazwa_eae58d_idx'),
        ),
        migrations.AddIndex(
            model_name='produkt',
            index=models.Index(fields=['numer_partii'], name='shop_produk_numer_p_1334a5_idx'),
        ),
        migrations.AddIndex(
            model_name='produkt',
            index=models.Index(fields=['cena'], name='shop_produk_cena_097924_idx'),
        ),
        migrations.AddIndex(
            model_name='produkt',
            index=models.Index(fields=['opis'], name='shop_produk_opis_b802d5_idx'),
        ),
        migrations.AddIndex(
            model_name='produkt',
            index=models.Index(fields=['liczba'], name='shop_produk_liczba_6f9814_idx'),
        ),
        migrations.AddIndex(
            model_name='produkt',
            index=models.Index(fields=['image'], name='shop_produk_image_6a8f02_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='czat',
            unique_together={('klient', 'producent')},
        ),
    ]
