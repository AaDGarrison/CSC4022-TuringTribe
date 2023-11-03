from django.urls import path
from . import views

urlpatterns = [
    path('setup-institution/', views.setupInstitution, ),
    path('send-link-request/', views.sendLinkRequest,),
    path('get-transactions/', views.getTransactions),
    path('get-balance/', views.getBalance),

    # Define more URL patterns as needed
]