from django.db import models


class Auto(models.Model):
    kenteken = models.CharField(max_length=10)
    bouwjaar = models.IntegerField(null=True, blank=True)
    prijs = models.IntegerField(null=True, blank=True)
    kilometer_stand = models.IntegerField(null=True, blank=True)
    vermogen = models.IntegerField(null=True, blank=True)
    isHandgeschakeld = models.BooleanField(null=True, blank=True)
    isBenzine = models.BooleanField(null=True, blank=True)
    url = models.CharField(max_length=500)