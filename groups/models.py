from email.message import EmailMessage
from tabnanny import verbose
from django.db import models

# Create your models here.


class PartyManager(models.Manager):
    def create_party(self, name, pwd, join, exch, spend):
        party = self.create(name=name, password=pwd, join_deadline=join, exchange_date=exch, spending_limit=spend)
        return party


class Party(models.Model):
    name = models.CharField(verbose_name="party name", max_length=60, unique=True)
    password = models.CharField(verbose_name="password", max_length=30, unique=True)
    join_deadline = models.DateField(verbose_name="deadline to join")
    exchange_date = models.DateField(verbose_name="date of gift exchange")
    spending_limit = models.SmallIntegerField(verbose_name="spending limit")
    landing_message = models.TextField(verbose_name="message on party landing page", blank=True)

    objects = PartyManager()

    def __str__ (self):
        return self.name




class Santa (models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email_address = models.EmailField(max_length=60)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    recipient = models.OneToOneField("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="gifter")

    def __str__(self):
        return self.first_name +' '+self.last_name

    class Meta():
        unique_together = [['email_address', 'party'], ['first_name', 'last_name', 'party']]
