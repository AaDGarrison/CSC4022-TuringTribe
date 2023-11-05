from django.urls import path
from . import views

urlpatterns = [
    path('setup-institution/', views.setupInstitution, ),
    path('send-link-request/', views.sendLinkRequest,),
    path('get-transactions/', views.getTransactions),
    path('get-balance/', views.getBalance),
    path('get-card-name/', views.getCardName),

    # Define more URL patterns as needed
]