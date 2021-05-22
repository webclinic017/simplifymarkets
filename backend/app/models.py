from django.utils.timezone import now
from django.db import models

""" Test table. """
class employee(models.Model):

    firstname = models.CharField(max_length = 10)
    lastname = models.CharField(max_length = 10)
    emp_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.firstname


""" Table for mined knowledge. """
class knowledge(models.Model):

    class Meta:
        verbose_name_plural = "knowledge"

    cagr = models.FloatField()
    highest = models.FloatField()
    currentPrice = models.FloatField(default=0.0)
    symbol = models.CharField(max_length = 16, primary_key=True)
    lastRun = models.DateTimeField(default=now)

    def __str__(self):
        return self.symbol
    