"""This file contains all the endpoint urls"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BiddingViewSet,
    get_biddings_by_ticket_id,
    login,
    logout,
    register,
    sell_ticket,
    TicketViewSet,
    UserViewSet,
)


router = DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'biddings', BiddingViewSet)
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('get-biddings-by-ticket-id/<int:ticket_id>/', get_biddings_by_ticket_id, name='get_biddings_by_ticket_id'),
    path('sell-ticket/<int:ticket_id>/', sell_ticket, name = 'sell-ticket'), 
    path('register/', register, name = 'register'),
    path('login/', login , name = 'login'),
    path('logout/', logout, name = 'logout'),
]
