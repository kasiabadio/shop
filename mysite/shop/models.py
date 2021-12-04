from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Kategoria(models.Model):
    id_kategorii = models.AutoField(primary_key=True)
    nazwa_kategorii = models.CharField(max_length=50, default="null")
    id_nadkategorii = models.IntegerField()
    
    # many-to-one with Kategoria
    podkategoria = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nazwa_kategorii
    

class Producent(models.Model):
    id_producenta = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=50, verbose_name="imię", default="null")
    nazwisko = models.CharField(max_length=50, default="null")
    adres = models.CharField(max_length=50, default="null")
    login = models.CharField(max_length=50)
    haslo = models.CharField(max_length=50, verbose_name="hasło")
    
    def __str__(self):
        return self.imie + " " + self.nazwisko
    
    
class Klient(AbstractBaseUser):
    id_klienta = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=50, verbose_name="imię", default="null")
    nazwisko = models.CharField(max_length=50, default="null")
    adres_dostawy = models.CharField(max_length=50, default="null")
    login = models.CharField(max_length=50)
    haslo = models.CharField(max_length=50, verbose_name="hasło")
    
    # custom user fields
    # email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    # username = login
    # date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    # last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    # is_admin = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    
    def __str__(self):
        return self.imie + " " + self.nazwisko


class Czat(models.Model):
    
    class Meta:
        # acts like a surrogate primary key
        unique_together = (('klient', 'producent'),)
    
    
    # many-to-one with klient
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    # klient = models.IntegerField()
    
    # many-to-one with producent
    producent = models.ForeignKey(Producent, on_delete=models.CASCADE)
    # producent = models.IntegerField()

    
class Wiadomosc(models.Model):
    
    class Meta:
        unique_together = (('id_wiadomosc', 'czat'),)
    
    id_wiadomosc = models.IntegerField(null=True)
    tresc = models.CharField(max_length=50, verbose_name="treść")
    data = models.DateField()
    czy_odczytana = models.BooleanField(default=False)
    flaga = models.BooleanField()
    
    # many-to-one with czat
    czat = models.ForeignKey(Czat, on_delete=models.CASCADE)
    
    
class Reklamacja(models.Model):
    tresc = models.CharField(max_length=1000, verbose_name="treść")
    typ_reklamacji = models.IntegerField()
    status = models.IntegerField() 



class Zamowienie(models.Model):
    objects = None
    
    # Why it didn't show in table?
    class Meta:
        unique_together = (('id_zamowienie', 'klient'),)
    
    id_zamowienie = models.IntegerField(null=True)
    czy_oplacone = models.BooleanField(verbose_name="czy opłacone")
    sposob_dostawy = models.CharField(max_length=50, verbose_name="sposób dostawy")
    status = models.IntegerField()
    koszt = models.FloatField()
    
    # problem jest taki, że chciałabym, żeby zamówienia, które są przypisane konkretnemu klientowi,
    # były podzielone na producentów, a na razie jest tak, że zamówienie musi mieć unikalnych producentów
    # może jak usunę to pole i będę sortowała po produktach (a każdy produkt ma przypisanego producenta, to się to da tak załatwić)
    # na razie jest ustawione na null
    
    # one-to-one with producent
    producent = OneToOneField(Producent, on_delete=models.SET_NULL, null=True)
    
    # one-to-one with czat
    czat = OneToOneField(Czat, on_delete=models.SET_NULL, null=True)
    
    # one-to-one with reklamacja
    reklamacja = OneToOneField(Reklamacja, on_delete=models.SET_NULL, null=True)
    
    # many-to-one with klient
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    
    
    
class Produkt(models.Model):
    objects = None
    
    nazwa = models.CharField(max_length=50)
    id_produktu = models.AutoField(primary_key=True)
    numer_partii = models.IntegerField()
    cena = models.FloatField()
    
    opis = models.CharField(max_length=1000, blank=True)
    liczba = models.IntegerField()

    # many-to-one with producent
    producent = models.ForeignKey(Producent, on_delete=models.CASCADE) 
    
    # many-to-one with zamowienie   
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.SET_NULL, null=True, verbose_name="zamówienie")
    
    # many-to-many with kategoria (it is saved in kategoria Class)
    kategoria = models.ManyToManyField(Kategoria) 

    image = models.ImageField(null=True, blank=True)
    

    @property
    def imageURL(self):
        if self.image:
            return getattr(self.image, 'url', None)
        return None
    