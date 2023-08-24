""" 
    This file is converting complex data types like
    Django models into native Python data types that can
    be easily rendered into JSON, XML, or other content types
"""
from rest_framework import serializers
from .models import Bidding, CustomUser, Ticket


class TicketSerializer(serializers.ModelSerializer):
    """ 
        Serializer for converting Ticket model
        instances to JSON and vice versa 
    """
    class Meta:
        """ 
            Assigns Ticket model to the model field
            and all the Ticket model instances to fields
        """
        model = Ticket
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    """ 
        Serializer for converting CustomUser model
        instances to JSON and vice versa 
    """        
    class Meta:
        """ 
            Assigns CustomUser to the model field
            and all the CustomUser model instances to fields
        """
        model = CustomUser
        fields = ('username', 'password', 'email', 'address')


class BiddingSerializer(serializers.ModelSerializer):
    """ 
        Serializer for converting Bidding model 
        instances to JSON and vice versa 
    """
    class Meta:
        """ 
            Assigns bidding to the model field 
            and all the Bidding model instances to fields 
        """
        model = Bidding
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    """ 
        Serializer for converting CustomUser model
        instances to JSON and vice versa
    """
    
    def create(self, validated_data):
        """ 
            This method creates the new user 
            and save it in the database
        """
        user = CustomUser.objects.create(
            email = validated_data.get('email'),
            username = validated_data.get('username'),
            address = validated_data.get('address')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    
    
    class Meta:
        """ 
            Assigns CustomUser to the model field and username,
            password, email and address to fields
        """
        model = CustomUser
        fields = ('username', 'password', 'email', 'address')
        