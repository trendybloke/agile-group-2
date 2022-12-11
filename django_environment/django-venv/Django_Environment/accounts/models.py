from django.db import models
from django.contrib.auth.models import AbstractUser #required for 2fa
import random

"""required for getting object url"""
from django.urls import reverse

"""required for refferencting the Django Auth tables as foreign keys"""
from django.conf import settings

"""Models defined below"""

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=12)

    def get_absolute_url(self):
        """Method to allow Access to an individual record from the browser"""
        return reverse('customuser_detail', args = [str(self.id)])
    
class Code(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.number = code_string
        super().save(*args, **kwargs)

class User_Details(models.Model):
    """Model to hold additional details required for a user to engage in EFT trading."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.RESTRICT, related_name = 'User')
    address_first_line = models.CharField(max_length = 255)
    address_second_line = models.CharField(blank = True, max_length = 255)
    address_city = models.CharField(max_length = 189)
    address_postcode = models.CharField(max_length = 8)
    ni = models.CharField(max_length = 9)
    passport_path = models.CharField(max_length = 255)
    card_number = models.CharField(max_length = 255)
    card_last_4 = models.CharField(max_length = 255)
    validated = models.BooleanField(default = False)
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.RESTRICT, related_name = 'Validated_by')

    def display_user(self):
        """Method to request linked user"""
        return self.user

    def display_validated_by(self):
        """Method to request linked validating user"""
        return self.validated_by

    def __str__(self):
        """Method to return a string representation of the user details."""
        return f'user: {self.user}, address_first_line: {self.address_first_line}, address_second_line: {self.address_second_line}, address_city: {self.address_city}, address_postcode: {self.address_postcode}, ni: {self.ni}, passport_path: {self.passport_path}, card_number: {self.card_number}, card_last_4: {self.card_last_4}, validated: {self.validated}, validated_by: {self.validated_by}'

class Account(models.Model):
    """Class To store a users balance details"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.RESTRICT)
    balance = models.DecimalField(decimal_places = 2 , max_digits = 10 )
    last_update = models.DateField()

    def display_user(self):
        """Method to request linked user"""
        return self.user

    def __str__(self):
        """Method to return a String representation of the Account"""
        return f'User: {self.user}, Balance: {self.balance}, last Updated: {self.last_update}'
    
    def update_balance(self,amount,type):
        """method to change balance of an account"""
        #find direction of funds from type #jp 9-12-2022, type expected is '-' to sub, '+' to add
        if type == "-":
            self.balance -= amount
        elif type == "+":
            self.balance += amount
        else:
            pass
        # add or subtract the amount depending on type
        print("balance edited") 
        
class Transaction_Type(models.Model):
    """Class to house the type and direction of transactions (either credit or debit)"""
    description = models.CharField(max_length = 255)
    direction = models.CharField(max_length = 255)

    def __str__(self):
        return f'Description: {self.description}, credit/debit: {self.direction}'


class Transaction(models.Model):
    """Class to store details about transactions eg trading EFT or changing account balance"""
    account = models.ForeignKey('Account', on_delete = models.RESTRICT)
    type = models.ForeignKey('Transaction_Type',on_delete = models.RESTRICT)
    amount = models.DecimalField(decimal_places = 2, max_digits = 10 )
    details = models.CharField(max_length = 255)

    def __str__(self):
        return f'account: {self.account}, type: {self.type}, amount: {self.amount}, details: {self.details}'

    def get_absolute_url(self):
        """Method to allow Access to an individual record from the browser"""
        return reverse('Transaction', args = [str(self.id)])

    def get_account(self):
        """Method to return the related account"""
        return self.account

    def get_type(self):
        """method to return the related Transaction type"""
        return self.type
class ETF(models.Model):
    """Model For Representing An ETF"""
    symbol = models.CharField(max_length = 20)
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
    price_on_create = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.RESTRICT, null = True, blank = True)

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


