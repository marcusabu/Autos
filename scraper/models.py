from django.db import models


class Auto(models.Model):
    titel = models.CharField(max_length=500, null=True, blank=True)
    upload_datum = models.DateTimeField(null=True, blank=True)
    kenteken = models.CharField(max_length=10)
    bouwjaar = models.IntegerField(null=True, blank=True)
    prijs = models.IntegerField(null=True, blank=True)
    kilometer_stand = models.IntegerField(null=True, blank=True)
    vermogen = models.IntegerField(null=True, blank=True)
    isHandgeschakeld = models.BooleanField(null=True, blank=True)
    isBenzine = models.BooleanField(null=True, blank=True)
    url = models.CharField(max_length=500)
