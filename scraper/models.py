from django.db import models


class Auto(models.Model):
    titel = models.CharField(max_length=500, null=True, blank=True)
    upload_datum = models.DateTimeField(null=True, blank=True)
    kenteken = models.CharField(max_length=10, unique=True)
    bouwjaar = models.IntegerField(null=True, blank=True)
    prijs = models.IntegerField(null=True, blank=True)
    kilometer_stand = models.IntegerField(null=True, blank=True)
    vermogen = models.IntegerField(null=True, blank=True)
    is_handgeschakeld = models.BooleanField(null=True, blank=True)
    is_benzine = models.BooleanField(null=True, blank=True)
    url = models.CharField(max_length=500)
    bron = models.CharField(max_length=100)
    apk = models.DateField(null=True, blank=True)
    merk = models.CharField(null=True, blank=True, max_length=30)
    model = models.CharField(null=True, blank=True, max_length=30)

    def __str__(self):
        return self.titel
