"""This file contains all the models for ticket-selling application"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """ 
        This model overrides AbstractUser model
        and adds extra field address
    """
    address = models.CharField(max_length=100, default= '')
    
    
class Ticket(models.Model):
    """ 
        This model is used for generating the ticket 
        with all the following fields
    """
    auctioneerId = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='tickets/')
    validity = models.DateTimeField()
    minPrice = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    details = models.TextField()
    categories = models.CharField(max_length=100)
    eventVenue = models.CharField(max_length=10)
    startingDate = models.DateTimeField()
    expiryDate = models.DateTimeField()
    isSold = models.BooleanField(default=False)
    bid = models.ForeignKey(
        'Bidding',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


class Bidding(models.Model):
    """This model is create a bid with following fields"""
    auctionerId = models.ForeignKey(
        CustomUser,
        related_name='biddings_as_auctioneer',
        on_delete=models.CASCADE
    )
    ticketId = models.ForeignKey(
        Ticket,
        related_name='biddings',
        on_delete=models.CASCADE
    )
    bidderId = models.ForeignKey(
        CustomUser,
        related_name='biddings_as_bidder',
        on_delete=models.CASCADE
    )
    biddingPrice = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    biddingDate = models.DateTimeField()
