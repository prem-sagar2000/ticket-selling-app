""" 
    This file handles request processing, and response generation. 
"""
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Bidding, CustomUser, Ticket
from .serializers import (
    BiddingSerializer,
    CustomUserSerializer,
    RegisterSerializer,
    TicketSerializer,
)


class TicketViewSet(viewsets.ModelViewSet):
    """ 
        It Handles CRUD operations for Tickets,
        requiring JWT authentication and permissions 
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer     
        
class UserViewSet(viewsets.ModelViewSet):
    """ It Handles CRUD operations for User,
        requiring JWT authentication and permissions """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
     
class BiddingViewSet(viewsets.ModelViewSet):
    """ It Handles CRUD operations for Bidding, 
        requiring JWT authentication and permissions """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Bidding.objects.all()
    serializer_class = BiddingSerializer
    
@api_view(['POST'], )
def register(request):
    """ 
        Accepts POST requests, uses RegisterSerializer to
        validate and create new users, and it returns success 
        response and user details 
    """
    serializer = RegisterSerializer(data = request.data)
    data = {}
    if serializer.is_valid():
        new_user = serializer.save()
        data['response'] = 'Account has been created'
        data['username'] = new_user.username
        data['email'] = new_user.email
    else:
        data = serializer.errors
        
    return Response(data)

@api_view(['POST'], )
@permission_classes([IsAuthenticated],)
@authentication_classes([JWTAuthentication])
def login(request):
    """ 
        Accepts POST requests, uses authenticate function to
        verify user credentials. it also generates refresh and
        access token and it returns success response and user details. 
    """
    user_name = request.data.get('username')
    user_password = request.data.get('password')
    user = authenticate(request, username = user_name, password = user_password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        return Response({
            'message' : 'Login Successful',
            'refresh_token' : refresh_token,
            'access_token' : access_token,
            'username' : user.username,
            'email' : user.email,
            'address' : user.address})
    else:
        return Response({
            'error': 'Invalid credentials'
        })
   
@api_view(['POST'], )
@permission_classes([IsAuthenticated], )
@authentication_classes([JWTAuthentication], )
def logout(request):
    """ 
        Accepts POST requests, and get the refresh token
        from request body and add that token in blacklist
    """
    try:
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'User Logged Out Successfully'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': 'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'], )
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_biddings_by_ticket_id(ticket_id):
    """ 
        This function returns all the biddings on 
        particular ticket by providing ticket id 
    """
    try:
        biddings = Bidding.objects.filter(ticketId=ticket_id)
        serializer = BiddingSerializer(biddings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Bidding.DoesNotExist:
        return Response(
            {'detail': 'No biddings found for the given ticket ID'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'], )
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def sell_ticket(request, ticket_id):
    """
        This function accepts POST requests. 
        It is used to sell the ticket to the specific bidder 
        by providing bidderId
    """
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        return Response(
            {'error': 'Ticket not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if ticket.isSold:
        return Response(
            {'error': 'Ticket is already sold'},
            status=status.HTTP_400_BAD_REQUEST
        )

    bidWinner = request.data.get('bidderId')
    if bidWinner:
        try:
            bidding = Bidding.objects.get(pk=bidWinner)
        except Bidding.DoesNotExist:
            return Response(
                {'error': 'Invalid bidder selected'}
                , status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.isSold = True
        ticket.bid = bidding 
        ticket.save()
        return Response(
            {'message': f'Ticket sold successfully to bidder with ID: {bidWinner}'},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'error': 'No bidder selected to sell the ticket'},
            status=status.HTTP_400_BAD_REQUEST
        )
   