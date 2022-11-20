from django.db import models

"""required for getting object url"""
from django.urls import reverse

"""required for refferencting the Django Auth tables as foreign keys"""
from django.conf import settings

"""Models defined below"""

class ETF(models.Model):
    """Model For Representing An ETF"""
    symbol = models.CharField(max_length = 6)
    date_created = models.DateField()
    is_deleted = models.BooleanField(default = False)

    def get_absolute_url(self):
        """Method to allow Access to an individual record from the browser"""
        return reverse('ETF-detail', args = [str(self.id)])

    def __str__(self):
        """Method to return a string representation of an an ETF (the symbol is used here)"""
        return f'{self.symbol}'

class ETF_instance(models.Model):
    """Model for representing an instance of an ETF"""
    date_created = models.DateField()
    is_deleted = models.BooleanField(default = False)
    ETF = models.ForeignKey('ETF', on_delete = models.RESTRICT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.RESTRICT, null = True)

    def display_ETF(self):
        """Method to request linked ETF"""
        return self.ETF

    def display_user(self):
        """Method to request linked user"""
        return self.user

    def get_absolute_url(self):
        """Method to allow Access to an individual record from the browser"""
        return reverse('ETF_instance_detail', args = [str(self.id)])

    def __str__(self):
        """Method to return a string representation of the ETF instance."""
        return f'ID: {self.id} ETF: {self.ETF} Date Created: {self.date_created} Owned By: {self.user}'



