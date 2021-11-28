from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField, OneToOneField


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
    
    
class Klient(models.Model):
    id_klienta = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=50, verbose_name="imię", default="null")
    nazwisko = models.CharField(max_length=50, default="null")
    adres_dostawy = models.CharField(max_length=50, default="null")
    login = models.CharField(max_length=50)
    haslo = models.CharField(max_length=50, verbose_name="hasło")
    
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
    
    # Why it didn't show in table?
    class Meta:
        unique_together = (('id_zamowienie', 'klient'),)
    
    id_zamowienie = models.IntegerField()
    czy_oplacone = models.BooleanField(verbose_name="czy opłacone")
    sposob_dostawy = models.CharField(max_length=50, verbose_name="sposób dostawy")
    status = models.IntegerField()
    koszt = models.FloatField()
    
    # one-to-one with producent
    producent = OneToOneField(Producent, on_delete=models.SET_NULL, null=True)
    
    # one-to-one with czat
    czat = OneToOneField(Czat, on_delete=models.SET_NULL, null=True)
    
    # one-to-one with reklamacja
    reklamacja = OneToOneField(Reklamacja, on_delete=models.SET_NULL, null=True)
    
    # many-to-one with klient
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    
    
    
class Produkt(models.Model):
    id_produktu = models.AutoField(primary_key=True)
    numer_partii = models.IntegerField()
    cena = models.FloatField()
    # What to do with desriptions?
    opis = models.CharField(max_length=1000, blank=True)
        
    
    # many-to-one with producent
    producent = models.ForeignKey(Producent, on_delete=models.CASCADE) 
    
    # many-to-one with zamowienie   
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.SET_NULL, null=True, verbose_name="zamówienie")
    
    # many-to-many with kategoria (it is saved in kategoria Class)
    kategoria = models.ManyToManyField(Kategoria) 
