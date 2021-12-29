from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField, OneToOneField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Kategoria(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['nazwa_kategorii'])
        ]
        
    id_kategorii = models.AutoField(primary_key=True)
    nazwa_kategorii = models.CharField(max_length=50, default="null")
    id_nadkategorii = models.IntegerField()
    
    # many-to-one with Kategoria
    podkategoria = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nazwa_kategorii
    


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, imie, nazwisko, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not imie:
            raise ValueError("Users must have name")
        if not nazwisko:
            raise ValueError("Users must have surname")
  
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            imie=imie,
            nazwisko=nazwisko
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, username, imie, nazwisko, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            imie=imie,
            nazwisko=nazwisko
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
 
class User(AbstractBaseUser):
    
    class Meta:
        indexes = [
            models.Index(fields=['imie',]),
            models.Index(fields=['nazwisko',]),
            models.Index(fields=['email',]),
            models.Index(fields=['username',]),
        ]
    
    id_user = models.AutoField(primary_key=True)
    is_producent = models.BooleanField(default=False)
    is_klient = models.BooleanField(default=False)
    imie = models.CharField(max_length=50, verbose_name="imię", default="null")
    nazwisko = models.CharField(max_length=50, default="null")

    email = models.EmailField(verbose_name="email", max_length=60, unique=True) 
    username = models.CharField(max_length=50)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # email will be used to login
    USERNAME_FIELD = 'email'
    # when register must have username
    REQUIRED_FIELDS = ['username', 'imie', 'nazwisko']
    
    objects = MyAccountManager()
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    
class Producent(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['adres',]),
        ]
        
    # custom producent fields
    id_producenta = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    adres = models.CharField(max_length=50, default="null")

       
class Klient(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['adres_dostawy',]),
        ]
        
    
    # custom user fields
    id_klienta = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    adres_dostawy = models.CharField(max_length=50, default="null")

    
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
        indexes = [
            models.Index(fields=['tresc',]),
            models.Index(fields=['data',]),
            models.Index(fields=['czy_odczytana',]),
            models.Index(fields=['flaga',]),
        ]
    
    id_wiadomosc = models.IntegerField(null=True)
    tresc = models.CharField(max_length=50, verbose_name="treść")
    data = models.DateField()
    czy_odczytana = models.BooleanField(default=False)
    flaga = models.BooleanField()
    
    # many-to-one with czat
    czat = models.ForeignKey(Czat, on_delete=models.CASCADE)
    
    
class Reklamacja(models.Model):
    
    class Meta:
        indexes = [
            models.Index(fields=['tresc',]),
            models.Index(fields=['typ_reklamacji',]),
            models.Index(fields=['status',]),
        ]
        
    tresc = models.CharField(max_length=1000, verbose_name="treść")
    typ_reklamacji = models.IntegerField()
    status = models.IntegerField() 



class Zamowienie(models.Model):
    objects = None
    
    class Meta:
        unique_together = (('id_zamowienie', 'klient'),)
        indexes = [
            models.Index(fields=['czy_oplacone',]),
            models.Index(fields=['sposob_dostawy',]),
            models.Index(fields=['status',]),
            models.Index(fields=['koszt',]),
        ]
    
    id_zamowienie = models.IntegerField(null=True)
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
    
    # product has many zamowienie, so we sum total of zamowienie where its id is in product
    @property
    def get_zamowienie_total(self):
        produktitems = self.produkt_set.all()
        total = sum([item.cena for item in produktitems])
        return total
    
    
class Produkt(models.Model):
    
    class Meta:
        
        indexes = [
            models.Index(fields=['nazwa',]),
            models.Index(fields=['numer_partii',]),
            models.Index(fields=['cena',]),
            models.Index(fields=['opis',]),
            models.Index(fields=['liczba',]),
            models.Index(fields=['image',]),
        ]
    
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
    